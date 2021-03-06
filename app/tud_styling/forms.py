from django import forms
from django.contrib.auth.models import User
from tud_styling.widgets import StylingDateInput, StylingTextInput, StylingUneditableInput

class TestForm(forms.Form):
#    date = forms.DateField(
#        widget=StylingDateInput(),
#    )
    my_date_field = forms.DateField(widget=forms.DateInput(
		attrs={'class': 'datepicker'}),
		label='mijn datum veld'
	)
    
    username = forms.CharField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
    url = forms.URLField()
    file = forms.FileField()
    image = forms.ImageField()
    multi = forms.MultipleChoiceField(
		choices=(
            ("apple", "Apple"),
            ("pear", "Pear"),
        ),
        widget = forms.SelectMultiple(
			attrs={
				'size': 2
			}
		),
        help_text=u'As you can see, multiple checkboxes work too',
    )

    title = forms.CharField(
		label='een titel',
        max_length=100,
        help_text='This is the standard text input',
    )
    body = forms.CharField(
        max_length=100,
        help_text=u'This is a text area',
        widget=forms.Textarea(
            attrs={
                'title': 'I am "nice"',
            }
        ),
    )
    disabled = forms.CharField(
        max_length=100,
        required=False,
        help_text=u'I am disabled',
        widget=forms.TextInput(attrs={
            'disabled': 'disabled',
            'placeholder': 'I am disabled',
        })
    )
    uneditable = forms.CharField(
        max_length=100,
        help_text=u'I am uneditable and you cannot enable me with JS',
        initial=u'Uneditable',
        widget=StylingUneditableInput()
    )
    content = forms.ChoiceField(
        choices=(
            ("text", "Plain text"),
            ("html", "HTML"),
        ),
        help_text=u'Pick your choice',
    )
    email = forms.EmailField()
    like = forms.BooleanField(required=False)
    fruits = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=(
            ("apple", "Apple"),
            ("pear", "Pear"),
        ),
        help_text=u'As you can see, multiple checkboxes work too',
    )
    number = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={
            'inline': True,
        }),
        choices=(
            ("3", "Three"),
            ("33", "Thirty three"),
            ("333", "Three hundred thirty three"),
        ),
        help_text=u'And can be inline',
    )
    color = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={'data-demo-attr': 'bazinga'}),
        choices=(
            ("#f00", "red"),
            ("#0f0", "green"),
            ("#00f", "blue"),
        ),
        help_text=u'And we have <i>radiosets</i>',
    )
    prepended = forms.CharField(
        max_length=100,
        help_text=u'I am prepended by a P',
        widget=StylingTextInput(prepend='P'),
    )

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data


class TestModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__' # Or a list of the fields that you want to include in your form
#        widgets = {'my_date_field': DateInput(attrs={'class': 'datepicker'})}

class TestInlineForm(forms.Form):
    query = forms.CharField(required=False, label="")
    vegetable = forms.ChoiceField(
        choices=(
            ("broccoli", "Broccoli"),
            ("carrots", "Carrots"),
            ("turnips", "Turnips"),
        ),
    )
    active = forms.ChoiceField(widget=forms.RadioSelect, label="", choices=(
        ('all', 'all'),
        ('active', 'active'),
        ('inactive', 'inactive')
        ), initial='all')
    mine = forms.BooleanField(required=False, label='Mine only', initial=False)


class WidgetsForm(forms.Form):
    date = forms.DateField(widget=StylingDateInput)


class FormSetInlineForm(forms.Form):
    foo = forms.CharField()
    bar = forms.CharField()
