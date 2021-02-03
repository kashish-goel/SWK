from django import forms
from .models import Tracksheet,DutyEntry,Zones,Feedback
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, ButtonHolder
import datetime
# from phonenumber_field.formfields import PhoneNumberField
from django.contrib.gis import forms

            
demarcated_lane = [('none','Select Zone'),
        ('Hira Seth Chawl to Waras Lane','Hira Seth Chawl to Waras Lane'),
        ('Navneet Lane to Tare Galli','Navneet Lane to Tare Galli'),
        ('Bhandar Wada to Amar Prem Chowk','Bhandar Wada to Amar Prem Chowk'),
        ('Shankar Mandir to Bhagat Galli ','Shankar Mandir to Bhagat Galli '),
        ('Gonta Galli to Kranti Galli','Gonta Galli to Kranti Galli'),
        ('Kranti Galli to Navjeevan Chowk','Kranti Galli to Navjeevan Chowk'),
        ('Pakhari Galli ','Pakhari Galli '),
        ('Bazar Galli to Fish market','Bazar Galli to Fish market'),
        ('Maval Maratha (Payari)', 'Maval Maratha'),
        ('Sonapur to Dukkur Galli','Sonapur to Dukkur Galli'),
        ('Dukkur Galli to Taak Galli','Dukkur Galli to Taak Galli'),
        ('Nagoba Ghumat to Achanak','Nagoba Ghumat to Achanak'),
        ('Golfadevi','Golfadevi'),
        
    ]
timeslot= [

            ('7:30am - 8:30 am','Morning'),
            ('7:30pm - 8:30 pm','Evening'),
        ]

Fatten_name = [
    ('Amrapali Nikalje','Amrapali Nikalje'),
    ('Kaushalya Maske', 'Kaushalya Maske'),
    ('Asha Sadar','Asha Sadar'),
    ('Kalinda Jogdand', 'Kalinda Jogdand'),
    ('Laxmi Gaoli','Laxmi Gaoli'),
    ('Jana pote','Jana pote'),
    ('Bismillah Saiyad','Bismillah Saiyad'),
    ('Rehana Saikh','Rehana Saikh'),
    ('Aruna Parkhe','Aruna Parkhe'),
    ('Ganga Sonavane','Ganga Sonavane'),
    ('Kavita Binniwale','Kavita Binniwale'),
    ('Sangeeta Gaikwad','Sangeeta Gaikwad'),
    ('Rama Sinde','Rama Sinde'),
    ('Sanjay Ahire','Sanjay Ahire'),
    
    

]

Satten_name = [
    ('Krushna Patekar', 'Krushna Patekar'),
    ('Parvati Yede','Parvati Yede'),
    ('Sakuntala Kahrat','Sakuntala Kahrat'),
    ('Amba Bai Isre', 'Amba Bai Isre'),
    ('Jija BaiMakasare','Jija BaiMakasare'),
    ('Vaishali Gaoli','Vaishali Gaoli'),
    ('Gaya Bai Parkhe','Gaya Bai Parkhe'),
    ('Indu Bai Gade','Indu Bai Gade'),
    ('Farzana Khan','Farzana Khan'),
    ('Santa Sinde','Santa Sinde'),
    ('Durga Ganbas','Durga Ganbas'),
    ('Sheema Sonavane','Sheema Sonavane'),
    ('Vinayak Salve','Vinayak Salve'),
    
]

supervisor_name = [
    ('Akshay Kharat','Akshay Kharat'),
    ('Sanjay Thorat','Sanjay Thorat'),
    ('Ankit Singh','Ankit Singh'),
    ('Umesh Salve','Umesh Salve'),
    ('Savita Sonawane','Savita Sonawane'),
    ('Zaheer','Zaheer'),
    ('Akash','Akash'),
]

class TracksheetForm(forms.ModelForm):
    
    date= forms.DateField(required=True,widget=forms.TextInput(attrs={'type': 'date'}),initial=datetime.date.today)
    lane_name = forms.CharField(label = 'Name of the Zone',widget=forms.Select(choices=demarcated_lane))
    first_attendants_name = forms.CharField(label = 'Name of First Attendant',widget=forms.Select(choices=Fatten_name))
    second_attendants_name = forms.CharField(label = 'Name of Second Attendant',widget=forms.Select(choices=Satten_name))
    supervisor_name = forms.CharField(label = 'Name of Supervisor',widget=forms.Select(choices=supervisor_name))
    num_houses_reached = forms.IntegerField(label = 'Houses Reached')
    time_of_visit = forms.CharField(label = "Morning /Evening Visit",widget=forms.Select(choices=timeslot))
    drywaste_bf = forms.IntegerField(label = "Dry waste before(kgs)")
    drywaste_af = forms.IntegerField(label = "Dry waste after(kgs)")
    wetwaste_bf = forms.IntegerField(label = "Wet waste before(kgs)")
    wetwaste_af = forms.IntegerField(label = "Wet waste after(kgs)")
    num_houses_doing_segg = forms.IntegerField(label = "No. of houses doing segregation")
    num_houses_giving_mixwaste = forms.IntegerField(label = "Houses giving mixed waste")
    rejected = forms.IntegerField(label="Rejected Waste:",widget=forms.HiddenInput(),required=False)
    zone_id_id=forms.CharField(max_length=10, label="Zone ID",widget=forms.HiddenInput(),required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['zone_id']=forms.ModelChoiceField(queryset=Zones.objects.filter(zone_name=user))

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('date', css_class='form-group col-md-3 mb-0'),
                Column('time_of_visit', css_class='form-group col-md-3 mb-0'),
                Column('lane_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            # 'address_1',
            # 'address_2',
            Row(
                Column('num_attendants', css_class='form-group col-md-3 mb-0'),
                Column('first_attendants_name', css_class='form-group col-md-3 mb-0'),
                Column('second_attendants_name', css_class='form-group col-md-3 mb-0'),
                Column('supervisor_name', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            # 'check_me_out',
            Row(
                Column('num_houses_reached', css_class='form-group col-md-4 mb-0'),
                Column('num_houses_doing_segg', css_class='form-group col-md-4 mb-0'),
                Column('num_houses_giving_mixwaste', css_class='form-group col-md-4 mb-0'),
                      
                css_class='form-row'
            ),
            Row(
                Column('drywaste_bf', css_class='form-group col-md-3 mb-0'),
                Column('drywaste_af', css_class='form-group col-md-3 mb-0'),
                Column('wetwaste_bf', css_class='form-group col-md-3 mb-0'),
                Column('wetwaste_af', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('rejected', css_class='form-group col-md-3 mb-0'),
                Column('zone_id_id', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            # rejected = forms.IntegerField(   
            #                             widget=forms.TextInput(attrs={'readonly':'readonly'})
            # ),
            # UneditableField('text_input', css_id="rejected"),
            
            Submit('submit', 'Save')
        )
       

    class Meta:

        model = Tracksheet
        fields = '__all__'
        exclude = ['zone_id']



class DutyEntryForm(forms.ModelForm):
    lane_name = forms.CharField(label = 'Name of the Route',widget=forms.Select(choices=demarcated_lane))
    first_attendants_name = forms.CharField(label = 'Name of First Attendant',widget=forms.Select(choices=Fatten_name))
    second_attendants_name = forms.CharField(label = 'Name of Second Attendant',widget=forms.Select(choices=Satten_name))
    num_houses_lane = forms.IntegerField(label = 'Houses in Lane')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            
            Row(
                Column('lane_name', css_class='form-group col-md-5 mb-0'),
                Column('num_houses_lane', css_class='form-group col-md-5 mb-0'),                
                css_class='form-row'
            ),
            
            Row(
                Column('first_attendants_name', css_class='form-group col-md-5 mb-0'),
                Column('second_attendants_name', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )

    class Meta:
        model = DutyEntry
        fields = '__all__'


    # name = forms.CharField(required=True)
    # email = forms.EmailField(required=False)
    # mobile = PhoneNumberField(required=True)
    
    # point = forms.PointField(required=True, widget=
    #     forms.OSMWidget(attrs={'map_width': 500, 'map_height': 300}))
    # feedback = forms.CharField(
    #     required=True,
    #     widget=forms.Textarea
    # )
class FeedbackForm(forms.ModelForm):
    # latitude = forms.CharField()
    # longitude = forms.CharField()
    name= forms.CharField()
    email = forms.CharField()
    mobile = forms.IntegerField()
    feedback = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20})
)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            
            Row(
                Column('latitude', css_class='form-group col-md-5 mb-0'),
                Column('longitude', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
            
            Row(
                Column('name', css_class='form-group col-md-5 mb-0'),                
                Column('email', css_class='form-group col-md-5 mb-0'),
                Column('mobile', css_class='form-group col-md-5 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('feedback', css_class='form-group col-md-5 mb-0'),
               
                css_class='form-row'
            ),
            Submit('submit', 'Save')
        )

    class Meta:
        model = Feedback
        fields = '__all__'
        exclude = ['latitude','longitude']

    
 
 