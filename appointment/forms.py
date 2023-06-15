from django import forms
from .models import Appointment, TakeAppointment


class CreateAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].label = "Full Name"
        self.fields['image'].label = "Image"
        self.fields['department'].label = "Department"
        self.fields['start_time'].label = "Start Time"
        self.fields['hospital_name'].label = "Hospital Name"
        self.fields['qualification_name'].label = "Qualification"
        self.fields['institute_name'].label = "Institute"

        self.fields['full_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Full Name',
            }
        )

        self.fields['department'].widget.attrs.update(
            {
                'placeholder': 'Select Your Service',
            }
        )

        self.fields['start_time'].widget.attrs.update(
            {
                'placeholder': 'Ex : 9 AM',
            }
        )
        self.fields['end_time'].widget.attrs.update(
            {
                'placeholder': 'Ex: 5 PM',
            }
        )
        self.fields['location'].widget.attrs.update(
            {
                'placeholder': 'Ex : Ghaziabad, India',
            }
        )

        self.fields['hospital_name'].widget.attrs.update(
            {
                'placeholder': 'Enter Hospital Name',
            }
        )

        self.fields['qualification_name'].widget.attrs.update(
            {
                'placeholder': 'Ex : MBBS, BDS',
            }
        )

        self.fields['institute_name'].widget.attrs.update(
            {
                'placeholder': 'Ex : DMC',
            }
        )

    class Meta:
        model = Appointment
        fields = ['full_name', 'image', 'department', 'start_time', 'end_time', 'location',
                  'hospital_name', 'qualification_name', 'institute_name']

    def is_valid(self):
        valid = super(CreateAppointmentForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        appointment = super(CreateAppointmentForm, self).save(commit=False)
        if commit:
            appointment.save()
        return appointment


class TakeAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TakeAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['appointment'].label = "Choose Your Doctor"
        self.fields['full_name'].label = "Full Name"
        self.fields['phone_number'].label = "Phone Number"
        self.fields['message'].label = "Message"

        self.fields['appointment'].widget.attrs.update(
            {
                'placeholder': 'Choose Your Doctor',
            }
        )

        self.fields['full_name'].widget.attrs.update(
            {
                'placeholder': 'Write Your Name',
            }
        )

        self.fields['phone_number'].widget.attrs.update(
            {
                'placeholder': 'Enter Phone Number',
            }
        )
        self.fields['message'].widget.attrs.update(
            {
                'placeholder': 'Write a short message',
            }
        )

    class Meta:
        model = TakeAppointment
        fields = ['appointment', 'full_name', 'phone_number', 'message']

    def is_valid(self):
        valid = super(TakeAppointmentForm, self).is_valid()

        # if already valid, then return True
        if valid:
            return valid
        return valid

    def save(self, commit=True):
        appointment = super(TakeAppointmentForm, self).save(commit=False)
        if commit:
            appointment.save()
        return appointment

class SymptomsForm(forms.Form):
  SYMPTOMS = [('Itching','Itching'), ('Skin Rash','Skin Rash'), ('Nodal Skin Eruptions','Nodal Skin Eruptions'), ('Continuous Sneezing','Continuous Sneezing'), ('Shivering','Shivering'), ('Chills','Chills'), ('Joint Pain','Joint Pain'), ('Stomach Pain','Stomach Pain'), ('Acidity','Acidity'), ('Ulcers On Tongue','Ulcers On Tongue'), ('Muscle Wasting','Muscle Wasting'), ('Vomiting','Vomiting'), ('Burning Micturition','Burning Micturition'), ('Spotting  Urination','Spotting  Urination'), ('Fatigue','Fatigue'), ('Weight Gain','Weight Gain'), ('Anxiety','Anxiety'), ('Cold Hands And Feets','Cold Hands And Feets'), ('Mood Swings','Mood Swings'), ('Weight Loss','Weight Loss'), ('Restlessness','Restlessness'), ('Lethargy','Lethargy'), ('Patches In Throat','Patches In Throat'), ('Irregular Sugar Level','Irregular Sugar Level'), ('Cough','Cough'), ('High Fever','High Fever'), ('Sunken Eyes','Sunken Eyes'), ('Breathlessness','Breathlessness'), ('Sweating','Sweating'), ('Dehydration','Dehydration'), ('Indigestion','Indigestion'), ('Headache','Headache'), ('Yellowish Skin','Yellowish Skin'), ('Dark Urine','Dark Urine'), ('Nausea','Nausea'), ('Loss Of Appetite','Loss Of Appetite'), ('Pain Behind The Eyes','Pain Behind The Eyes'), ('Back Pain','Back Pain'), ('Constipation','Constipation'), ('Abdominal Pain','Abdominal Pain'), ('Diarrhoea','Diarrhoea'), ('Mild Fever','Mild Fever'), ('Yellow Urine','Yellow Urine'), ('Yellowing Of Eyes','Yellowing Of Eyes'), ('Acute Liver Failure','Acute Liver Failure'), ('Fluid Overload','Fluid Overload'), ('Swelling Of Stomach','Swelling Of Stomach'), ('Swelled Lymph Nodes','Swelled Lymph Nodes'), ('Malaise','Malaise'), ('Blurred And Distorted Vision','Blurred And Distorted Vision'), ('Phlegm','Phlegm'), ('Throat Irritation','Throat Irritation'), ('Redness Of Eyes','Redness Of Eyes'), ('Sinus Pressure','Sinus Pressure'), ('Runny Nose','Runny Nose'), ('Congestion','Congestion'), ('Chest Pain','Chest Pain'), ('Weakness In Limbs','Weakness In Limbs'), ('Fast Heart Rate','Fast Heart Rate'), ('Pain During Bowel Movements','Pain During Bowel Movements'), ('Pain In Anal Region','Pain In Anal Region'), ('Bloody Stool','Bloody Stool'), ('Irritation In Anus','Irritation In Anus'), ('Neck Pain','Neck Pain'), ('Dizziness','Dizziness'), ('Cramps','Cramps'), ('Bruising','Bruising'), ('Obesity','Obesity'), ('Swollen Legs','Swollen Legs'), ('Swollen Blood Vessels','Swollen Blood Vessels'), ('Puffy Face And Eyes','Puffy Face And Eyes'), ('Enlarged Thyroid','Enlarged Thyroid'), ('Brittle Nails','Brittle Nails'), ('Swollen Extremeties','Swollen Extremeties'), ('Excessive Hunger','Excessive Hunger'), ('Extra Marital Contacts','Extra Marital Contacts'), ('Drying And Tingling Lips','Drying And Tingling Lips'), ('Slurred Speech','Slurred Speech'), ('Knee Pain','Knee Pain'), ('Hip Joint Pain','Hip Joint Pain'), ('Muscle Weakness','Muscle Weakness'), ('Stiff Neck','Stiff Neck'), ('Swelling Joints','Swelling Joints'), ('Movement Stiffness','Movement Stiffness'), ('Spinning Movements','Spinning Movements'), ('Loss Of Balance','Loss Of Balance'), ('Unsteadiness','Unsteadiness'), ('Weakness Of One Body Side','Weakness Of One Body Side'), ('Loss Of Smell','Loss Of Smell'), ('Bladder Discomfort','Bladder Discomfort'), ('Foul Smell Of Urine','Foul Smell Of Urine'), ('Continuous Feel Of Urine','Continuous Feel Of Urine'), ('Passage Of Gases','Passage Of Gases'), ('Internal Itching','Internal Itching'), ('Toxic Look (Typhos)','Toxic Look (Typhos)'), ('Depression','Depression'), ('Irritability','Irritability'), ('Muscle Pain','Muscle Pain'), ('Altered Sensorium','Altered Sensorium'), ('Red Spots Over Body','Red Spots Over Body'), ('Belly Pain','Belly Pain'), ('Abnormal Menstruation','Abnormal Menstruation'), ('Dischromic  Patches','Dischromic  Patches'), ('Watering From Eyes','Watering From Eyes'), ('Increased Appetite','Increased Appetite'), ('Polyuria','Polyuria'), ('Family History','Family History'), ('Mucoid Sputum','Mucoid Sputum'), ('Rusty Sputum','Rusty Sputum'), ('Lack Of Concentration','Lack Of Concentration'), ('Visual Disturbances','Visual Disturbances'), ('Receiving Blood Transfusion','Receiving Blood Transfusion'), ('Receiving Unsterile Injections','Receiving Unsterile Injections'), ('Coma','Coma'), ('Stomach Bleeding','Stomach Bleeding'), ('Distention Of Abdomen','Distention Of Abdomen'), ('History Of Alcohol Consumption','History Of Alcohol Consumption'), ('Fluid Overload','Fluid Overload'), ('Blood In Sputum','Blood In Sputum'), ('Prominent Veins On Calf','Prominent Veins On Calf'), ('Palpitations','Palpitations'), ('Painful Walking','Painful Walking'), ('Pus Filled Pimples','Pus Filled Pimples'), ('Blackheads','Blackheads'), ('Scurring','Scurring'), ('Skin Peeling','Skin Peeling'), ('Silver Like Dusting','Silver Like Dusting'), ('Small Dents In Nails','Small Dents In Nails'), ('Inflammatory Nails','Inflammatory Nails'), ('Blister','Blister'), ('Red Sore Around Nose','Red Sore Around Nose'), ('Yellow Crust Ooze','Yellow Crust Ooze'), ('Prognosis','Prognosis')]
  
  symptoms = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=SYMPTOMS)
    