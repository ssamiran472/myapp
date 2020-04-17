from django import forms
from django.forms import ModelForm
from users.models import Foods, Category, Restaurents
from django.contrib.auth.models import User


class name_users(forms.Form):
    username = forms.CharField(max_length=20, label='username')
    password = forms.CharField(label='password', widget=forms.PasswordInput)

class new_user(forms.Form):
    username = forms.CharField(max_length=15, label='username')
    f_name = forms.CharField(max_length=15, label='f_name')
    l_name = forms.CharField(label='l_name', max_length=15)
    email = forms.EmailField(label='email')
    password =forms.CharField(label='password', widget=forms.PasswordInput)
    conf_password =forms.CharField(label='confirm password', widget=forms.PasswordInput)




class resturent(forms.ModelForm):
    
    class Meta:
        model = Restaurents
        fields = ["name","address","mob_no", "city", "country", "pincode", "locality", "restaurent_Main_img"]
        labels = {
                'name'   : "Restaurent's name",
                'address'       : 'Full address',
                'mob_no'       : 'Mob no',
                'city' : 'City name',
                'country' : 'Country name',
                'pincode' : 'Pin',
                'locality' : 'locality',
                'restaurent_Main_img' : 'Restaurents photo'
        }


my_choice = ( 
    ("Adhar card", "Adhar card"), 
    ("Voter id", "voter card"), 
    ("Driving lisence", "Driving lisence"), 
    ("Passport", "Passport"), 
    ("Pan card", "Pan card"), 
)

class deliveryPartner(forms.Form):
    
    name = forms.CharField(max_length = 20, label='full name')
    password = forms.CharField(max_length=10, widget=forms.PasswordInput, label='Password')
    mob_no = forms.CharField(label= 'Mobile no', min_length=10, max_length=12)
    email = forms.EmailField(label = 'Email')
    identy_proof = forms.ChoiceField(choices = my_choice) 
    photo = forms.ImageField(label = 'photo of identy proof') 
    driving_licence = forms.ImageField(label='photo of your driving licence')
    vachile_type = forms.CharField(label='Vachile Type')
    vachile_no = forms.CharField(label='Vachile No')
    locality = forms.CharField(label='Locality')

class foods(forms.ModelForm):
    category = forms.ModelChoiceField(
        widget       = forms.Select,
        queryset     = None,
        required     = False,
        empty_label  = None,
        to_field_name= None,
        label        = 'category'
        ) 
 
    def __init__(self, user, *args, **kwargs):
        super(foods, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all().filter(restaurent=user)

    
    class Meta:
        model = Foods
        fields = ['foods_name', 'category', 'price', 'image', 'description']
        labels = {
                'food_name'   : "food's name",
                'price'       : 'price',
                'image'       : 'image',
                'description' : 'description'
        }