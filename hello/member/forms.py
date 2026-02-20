from django import forms
from django.db.models import Q

from .models import City, Country, Member, MemberDetail, State


class MemberForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["country"].queryset = Country.objects.all().order_by("name")
        self.fields["state"].queryset = State.objects.none()
        self.fields["city"].queryset = City.objects.none()

        country_id = self.data.get("country")
        state_id = self.data.get("state")

        if not country_id and self.instance and self.instance.country_id:
            country_id = self.instance.country_id
        if not state_id and self.instance and self.instance.state_id:
            state_id = self.instance.state_id

        if country_id:
            self.fields["state"].queryset = State.objects.filter(country_id=country_id).order_by("name")
            self.fields["city"].queryset = City.objects.filter(country_id=country_id).order_by("name")

        if state_id:
            self.fields["city"].queryset = self.fields["city"].queryset.filter(
                Q(state_id=state_id) | Q(state__isnull=True)
            )

    class Meta:
        model = Member
        fields = [
            "first_name",
            "middle_name",
            "surname",
            "phone_no",
            "date_of_birth",
            "age",
            "gender",
            "occupation",
            "email_id",
            "country",
            "state",
            "city",
            "residential_address",
            "profile_image",
            "marital_status",
            "education",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
            "phone_no": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "occupation": forms.TextInput(attrs={"class": "form-control"}),
            "email_id": forms.EmailInput(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-control"}),
            "state": forms.Select(attrs={"class": "form-control"}),
            "city": forms.Select(attrs={"class": "form-control"}),
            "residential_address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "profile_image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "marital_status": forms.Select(attrs={"class": "form-control"}),
            "education": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get("country")
        state = cleaned_data.get("state")
        city = cleaned_data.get("city")

        if state and country and state.country_id != country.id:
            self.add_error("state", "Selected state does not belong to selected country.")

        if city and country and city.country_id != country.id:
            self.add_error("city", "Selected city does not belong to selected country.")

        if city and state and city.state_id and city.state_id != state.id:
            self.add_error("city", "Selected city does not belong to selected state.")

        return cleaned_data


class MemberCreateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
            "first_name",
            "middle_name",
            "surname",
            "phone_no",
            "email_id",
            "gender",
            "date_of_birth",
            "occupation",
            "country",
            "state",
            "city",
            "residential_address",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["middle_name"].required = False
        self.fields["email_id"].required = True
        self.fields["date_of_birth"].required = False
        self.fields["occupation"].required = False
        self.fields["country"].required = True
        self.fields["state"].required = True
        self.fields["city"].required = False
        self.fields["residential_address"].required = True

        self.fields["country"].queryset = Country.objects.all().order_by("name")
        self.fields["state"].queryset = State.objects.none()
        self.fields["city"].queryset = City.objects.none()

        country_id = self.data.get("country") or self.initial.get("country")
        state_id = self.data.get("state") or self.initial.get("state")

        if country_id:
            self.fields["state"].queryset = State.objects.filter(country_id=country_id).order_by("name")
            self.fields["city"].queryset = City.objects.filter(country_id=country_id).order_by("name")

        if state_id:
            self.fields["city"].queryset = self.fields["city"].queryset.filter(
                Q(state_id=state_id) | Q(state__isnull=True)
            )

    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get("country")
        state = cleaned_data.get("state")
        city = cleaned_data.get("city")

        if state and country and state.country_id != country.id:
            self.add_error("state", "Selected state does not belong to selected country.")

        if city and country and city.country_id != country.id:
            self.add_error("city", "Selected city does not belong to selected country.")

        if city and state and city.state_id and city.state_id != state.id:
            self.add_error("city", "Selected city does not belong to selected state.")

        return cleaned_data


class MemberDetailForm(forms.ModelForm):
    class Meta:
        model = MemberDetail
        fields = [
            "first_name",
            "middle_name",
            "surname",
            "date_of_birth",
            "age",
            "gender",
            "occupation",
            "email_id",
            "profile_image",
            "marital_status",
            "education",
        ]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "middle_name": forms.TextInput(attrs={"class": "form-control"}),
            "surname": forms.TextInput(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "occupation": forms.TextInput(attrs={"class": "form-control"}),
            "email_id": forms.EmailInput(attrs={"class": "form-control"}),
            "profile_image": forms.ClearableFileInput(attrs={"class": "form-control-file"}),
            "marital_status": forms.Select(attrs={"class": "form-control"}),
            "education": forms.TextInput(attrs={"class": "form-control"}),
        }
