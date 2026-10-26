import pytest
from django.urls import reverse
from shelter.models import Animal, AnimalType, CustomUser, Breed
from django.conf import settings
from shelter.forms import AnimalListingForm
from datetime import date

@pytest.fixture
def animal_types(db):
    dog_type = AnimalType.objects.create(name="Dog")
    cat_type = AnimalType.objects.create(name="Cat")
    return dog_type, cat_type


@pytest.fixture
def animals(db, animal_types, django_user_model):
    dog_type, cat_type = animal_types

    poster = django_user_model.objects.create_user(
        username="test_poster",
        password="test-password",
    )

    available_dog = Animal.objects.create(
        name="Buddy",
        posted_by=poster,
        animal_type=dog_type,
        age=3,
        weight="12.50",
        status="available",
    )
    available_cat = Animal.objects.create(
        name="Mittens",
        posted_by=poster,
        animal_type=cat_type,
        age=2,
        weight="4.20",
        status="available",
    )
    pending_dog = Animal.objects.create(
        name="Rex",
        posted_by=poster,
        animal_type=dog_type,
        age=5,
        weight="20.00",
        status="pending",
    )

    return available_dog, available_cat, pending_dog


@pytest.mark.django_db
def test_animal_list_shows_only_available_animals(client, animals):
    response = client.get(reverse("shelter:animal_list"))

    assert response.status_code == 200

    listed_animals = list(response.context["animals"])
    assert {animal.name for animal in listed_animals} == {"Buddy", "Mittens"}


@pytest.mark.django_db
def test_animal_list_filters_by_animal_type(client, animals, animal_types):
    dog_type, _ = animal_types

    response = client.get(
        reverse("shelter:animal_list"),
        {"animal_type": str(dog_type.pk)},
    )

    assert response.status_code == 200
    assert [animal.name for animal in response.context["animals"]] == ["Buddy"]
    assert response.context["selected_animal_type"] == dog_type.pk


@pytest.mark.django_db
def test_animal_list_handles_non_numeric_type_filter(client, animals):
    response = client.get(
        reverse("shelter:animal_list"),
        {"animal_type": "abc"},
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_animal_list_handles_unknown_type_id(client, animals):
    response = client.get(
        reverse("shelter:animal_list"),
        {"animal_type": "999999"},
    )

    assert response.status_code == 200
    assert list(response.context["animals"]) == []


@pytest.mark.django_db
def test_animal_list_handles_empty_type_filter(client, animals):
    response = client.get(
        reverse("shelter:animal_list"),
        {"animal_type": ""},
    )

    assert response.status_code == 200
    assert {animal.name for animal in response.context["animals"]} == {
        "Buddy",
        "Mittens",
    }

@pytest.mark.django_db
def test_animal_detail_displays_existing_animal(client, animals):
    animal = animals[0]

    response = client.get(
        reverse("shelter:animal_detail", kwargs={"pk": animal.pk})
    )

    assert response.status_code == 200
    assert response.context["animal"].pk == animal.pk


@pytest.mark.django_db
def test_animal_detail_returns_404_for_missing_animal(client):
    response = client.get(
        reverse("shelter:animal_detail", kwargs={"pk": 999999})
    )

    assert response.status_code == 404



@pytest.fixture
def valid_signup_data():
    return {
        "account_type": "individual",
        "username": "test_adopter",
        "email": "adopter@example.com",
        "full_name": "Test Adopter",
        "phone": "1001234567",
        "governorate": "alexandria",
        "address": "Alexandria, Egypt",
        "password1": "SafeTestPassword!739",
        "password2": "SafeTestPassword!739",
    }


@pytest.mark.django_db
def test_signup_creates_user_and_logs_them_in(client, valid_signup_data):
    response = client.post(
        reverse("shelter:signup"),
        valid_signup_data,
    )

    assert response.status_code == 302
    assert CustomUser.objects.filter(username="test_adopter").exists()
    assert "_auth_user_id" in client.session


@pytest.mark.django_db
def test_signup_invalid_data_does_not_create_user(client, valid_signup_data):
    valid_signup_data["password2"] = "DifferentPassword!739"

    response = client.post(
        reverse("shelter:signup"),
        valid_signup_data,
    )

    assert response.status_code == 200
    assert not CustomUser.objects.filter(username="test_adopter").exists()
    assert response.context["form"].errors


@pytest.mark.django_db
def test_signup_uses_default_redirect_when_next_is_missing(
    client, valid_signup_data
):
    response = client.post(
        reverse("shelter:signup"),
        valid_signup_data,
    )

    assert response.status_code == 302
    assert response.url == reverse(settings.LOGIN_REDIRECT_URL)


@pytest.mark.django_db
def test_signup_does_not_redirect_to_external_next_url(
    client, valid_signup_data
):
    response = client.post(
        f"{reverse('shelter:signup')}?next=https://example.com/phishing",
        valid_signup_data,
    )

    assert response.status_code == 302
    assert response.url != "https://example.com/phishing"


@pytest.mark.django_db
def test_signup_allows_safe_local_next_url(client, valid_signup_data):
    next_url = "/animals/"

    response = client.post(
        f"{reverse('shelter:signup')}?next={next_url}",
        valid_signup_data,
    )

    assert response.status_code == 302
    assert response.url == next_url

@pytest.mark.django_db
def test_signup_rejects_protocol_relative_next_url(
    client,
    valid_signup_data,
):
    response = client.post(
        f"{reverse('shelter:signup')}?next=//evil.example",
        valid_signup_data,
    )

    assert response.status_code == 302
    assert response.url == reverse(settings.LOGIN_REDIRECT_URL)


@pytest.mark.django_db
def test_shelter_signup_creates_shelter_profile(
    client, valid_signup_data
):
    valid_signup_data["account_type"] = "shelter"

    response = client.post(
        reverse("shelter:signup"),
        valid_signup_data,
    )

    assert response.status_code == 302

    user = CustomUser.objects.get(username="test_adopter")

    assert user.account_type == "shelter"
    assert user.shelter_profile.name == user.full_name
    assert user.shelter_profile.contact_email == user.email
    
    
@pytest.mark.django_db
def test_animal_listing_form_accepts_matching_breed_and_animal_type(animal_types):
    dog_type, _ = animal_types
    dog_breed = Breed.objects.create(
        name="Labrador",
        animal_type=dog_type,
    )
    form = AnimalListingForm(
        data={
            "name" : "Buddy",
            "animal_type": str(dog_type.pk),
            "breed" : str(dog_breed.pk),
            "age" : 3,
            "weight" : "12.50",
            "gender": "M",
            "arrival_date": "2026-01-15",
        }
    )
    assert form.is_valid(), form.errors
    
@pytest.mark.django_db
def test_animal_listing_form_rejects_mismatched_breed(animal_types):
    dog_type, cat_type = animal_types
    cat_breed = Breed.objects.create(
        name="Persian",
        animal_type=cat_type,
    )

    form = AnimalListingForm(
        data={
            "name": "Buddy",
            "animal_type": str(dog_type.pk),
            "breed": str(cat_breed.pk),
            "age": "3",
            "weight": "12.50",
            "gender": "M",
            "arrival_date": "2026-01-15",
        }
    )

    assert not form.is_valid()
    assert "breed" in form.errors


@pytest.mark.django_db
def test_animal_listing_form_accepts_missing_optional_breed(animal_types):
    dog_type, _ = animal_types

    form = AnimalListingForm(
        data={
            "name": "Buddy",
            "animal_type": str(dog_type.pk),
            "breed": "",
            "age": "3",
            "weight": "12.50",
            "gender": "M",
            "arrival_date": "2026-01-15",
        }
    )

    assert form.is_valid(), form.errors


@pytest.mark.django_db
def test_animal_listing_form_rejects_missing_name(animal_types):
    dog_type, _ = animal_types

    form = AnimalListingForm(
        data={
            "animal_type": str(dog_type.pk),
            "breed": "",
            "age": "3",
            "weight": "12.50",
            "gender": "M",
            "arrival_date": "2026-01-15",
        }
    )

    assert not form.is_valid()
    assert "name" in form.errors
    
    
@pytest.mark.django_db
def test_anonymous_user_cannot_create_animal_listing(client):
    response = client.get(reverse("shelter:animal_create"))

    assert response.status_code == 302
    assert reverse("shelter:login") in response.url


@pytest.mark.django_db
def test_authenticated_user_can_create_animal_listing(
    client, django_user_model, animal_types
):
    user = django_user_model.objects.create_user(
        username="listing_creator",
        password="SafeTestPassword!739",
    )
    dog_type, _ = animal_types
    client.force_login(user)

    response = client.post(
        reverse("shelter:animal_create"),
        {
            "name": "Buddy",
            "animal_type": str(dog_type.pk),
            "breed": "",
            "gender": "M",
            "age": "3",
            "weight": "12.50",
            "description": "Friendly dog",
            "arrival_date": "2026-01-15",
            "special_needs": "",
            "is_vaccinated": "on",
            "is_spayed_neutered": "",
        },
    )

    assert response.status_code == 302

    animal = Animal.objects.get(name="Buddy")
    assert animal.posted_by == user
    assert animal.status == "available"
    assert animal.is_vaccinated is True

    assert response.url == reverse(
        "shelter:animal_detail",
        kwargs={"pk": animal.pk},
    )


@pytest.mark.django_db
def test_invalid_animal_listing_is_not_saved(
    client, django_user_model, animal_types
):
    user = django_user_model.objects.create_user(
        username="invalid_listing_user",
        password="SafeTestPassword!739",
    )
    dog_type, _ = animal_types
    client.force_login(user)

    response = client.post(
        reverse("shelter:animal_create"),
        {
            "name": "",
            "animal_type": str(dog_type.pk),
            "breed": "",
            "gender": "M",
            "age": "3",
            "weight": "12.50",
            "arrival_date": "2026-01-15",
        },
    )

    assert response.status_code == 200
    assert response.context["form"].errors
    assert not Animal.objects.filter(
        posted_by=user
    ).exists()


@pytest.mark.django_db
def test_animal_listing_ignores_forged_owner_and_status(
    client, django_user_model, animal_types
):
    user = django_user_model.objects.create_user(
        username="real_poster",
        password="SafeTestPassword!739",
    )
    other_user = django_user_model.objects.create_user(
        username="other_user",
        password="SafeTestPassword!739",
    )
    dog_type, _ = animal_types
    client.force_login(user)

    response = client.post(
        reverse("shelter:animal_create"),
        {
            "name": "Buddy",
            "animal_type": str(dog_type.pk),
            "breed": "",
            "gender": "M",
            "age": "3",
            "weight": "12.50",
            "arrival_date": "2026-01-15",
            "posted_by": str(other_user.pk),
            "status": "adopted",
        },
    )

    assert response.status_code == 302

    animal = Animal.objects.get(name="Buddy")
    assert animal.posted_by == user
    assert animal.status == "available"
