from django import forms

class GiftRecommendationForm(forms.Form):
    BUDGET_MIN = 1

    occasion = forms.ChoiceField(choices=[
        ("Birthday", "Birthday"),
        ("Graduation", "Graduation"),
        ("MothersDay", "Mother's Day"),
        ("GetWellSoon", "Get well soon"),
        ("Anniversary", "Anniversary"),
        ("Other", "Other"),
    ])

    budget = forms.DecimalField(min_value=BUDGET_MIN, decimal_places=2, max_digits=10)

    gender = forms.ChoiceField(required=False, choices=[
        ("", "Any"),
        ("Female", "Female"),
        ("Male", "Male"),
    ])

    age_range = forms.ChoiceField(required=False, choices=[
        ("", "Any"),
        ("Child", "Child"),
        ("Teen", "Teen"),
        ("Adult", "Adult"),
        ("Senior", "Senior"),
    ])

    relationship = forms.ChoiceField(required=False, choices=[
        ("", "Any"),
        ("Mother", "Mother"),
        ("Friend", "Friend"),
        ("Colleague", "Colleague"),
    ])
