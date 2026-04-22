from django import forms

from .models import Bazaar


class BazaarForm(forms.ModelForm):
    class Meta:
        model = Bazaar
        fields = [
            'title',
            'description',
            'main_image',
            'location',
            'start_datetime',
            'end_datetime',
            'table_price',
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-900',
                    'autocomplete': 'off',
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-900',
                }
            ),
            'main_image': forms.FileInput(
                attrs={
                    'class': 'block w-full text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-gradient-to-r file:from-orange-400 file:to-pink-500 file:text-white',
                }
            ),
            'location': forms.TextInput(
                attrs={
                    'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-900',
                    'autocomplete': 'off',
                }
            ),
            'start_datetime': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'step': '60',
                    'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-900',
                },
            ),
            'end_datetime': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={
                    'type': 'datetime-local',
                    'step': '60',
                    'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-900',
                },
            ),
            'table_price': forms.NumberInput(
                attrs={
                    'class': 'w-full border border-gray-300 rounded-lg px-3 py-2 text-gray-900',
                    'step': '0.01',
                    'min': '0',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dt_formats = ['%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S']
        self.fields['start_datetime'].input_formats = dt_formats
        self.fields['end_datetime'].input_formats = dt_formats
