from collections import defaultdict
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from accounts.models import User
from appointment.ml_alogorithm import predict_disease
from .decorators import user_is_patient, user_is_doctor
from django.views.generic import TemplateView, UpdateView, CreateView, ListView, DetailView, DeleteView
from django.views.generic.edit import DeleteView, UpdateView
from accounts.forms import PatientProfileUpdateForm, DoctorProfileUpdateForm
from .forms import CreateAppointmentForm, SymptomsForm, TakeAppointmentForm
from .models import Appointment, ReportImages, TakeAppointment
from django.template.defaulttags import register

"""
For Patient Profile
    
"""
disease_dictionary = {
    'Varicose veins': {
        'symptoms': ['Enlarged veins', 'Swelling', 'Aching or pain', 'Heavy feeling'],
        'precautions': ['Avoid standing or sitting for long periods', 'Elevate your legs', 'Regular exercise', 'Wear compression stockings']
    },
    'Urinary tract infection': {
        'symptoms': ['Burning sensation during urination', 'Frequent urination', 'Cloudy or bloody urine', 'Lower abdominal pain'],
        'precautions': ['Drink plenty of water', 'Urinate when you feel the need', 'Wipe from front to back after using the toilet', 'Avoid irritating feminine products']
    },
    'Typhoid': {
        'symptoms': ['High fever', 'Weakness', 'Stomach pain', 'Headache'],
        'precautions': ['Drink clean and purified water', 'Eat thoroughly cooked food', 'Maintain good personal hygiene', 'Get vaccinated']
    },
    'Tuberculosis': {
        'symptoms': ['Cough with blood', 'Chest pain', 'Fatigue', 'Weight loss'],
        'precautions': ['Complete the full course of medication', 'Cover your mouth while coughing or sneezing', 'Avoid close contact with infected individuals', 'Improve ventilation in living spaces']
    },
    'Psoriasis': {
        'symptoms': ['Red patches of skin with silvery scales', 'Dry and cracked skin', 'Itching', 'Thickened and pitted nails'],
        'precautions': ['Keep your skin moisturized', 'Avoid triggers like stress and certain medications', 'Use medicated creams or ointments as prescribed', 'Protect your skin from injury or sunburn']
    },
    'Pneumonia': {
        'symptoms': ['Chest pain', 'Fever', 'Cough with phlegm', 'Shortness of breath'],
        'precautions': ['Get vaccinated against pneumonia', 'Wash your hands regularly', 'Cover your mouth and nose when coughing or sneezing', 'Avoid smoking and secondhand smoke']
    },
    'Peptic ulcer disease': {
        'symptoms': ['Abdominal pain', 'Burning sensation in the stomach', 'Nausea', 'Vomiting'],
        'precautions': ['Avoid spicy and acidic foods', 'Limit alcohol consumption', 'Quit smoking', 'Manage stress levels']
    },
    'Paralysis (brain hemorrhage)': {
        'symptoms': ['Loss of movement or sensation', 'Severe headache', 'Difficulty speaking or understanding', 'Loss of consciousness'],
        'precautions': ['Seek immediate medical attention', 'Follow prescribed treatment and rehabilitation plans', 'Take measures to prevent further strokes', 'Manage underlying conditions like high blood pressure']
    },
    'Osteoarthritis': {
        'symptoms': ['Joint pain', 'Stiffness', 'Swelling', 'Limited range of motion'],
        'precautions': ['Maintain a healthy weight', 'Exercise regularly to strengthen muscles', 'Apply hot or cold packs to affected joints', 'Use assistive devices if necessary']
    },
    'Migraine': {
        'symptoms': ['Severe headache', 'Nausea', 'Sensitivity to light and sound', 'Aura'],
        'precautions': ['Identify and avoid triggers', 'Maintain a regular sleep schedule', 'Practice relaxation techniques', 'Take prescribed medications']
    },
    'Malaria': {
        'symptoms': ['Fever', 'Chills', 'Headache', 'Sweating'],
        'precautions': ['Use mosquito nets or insect repellents', 'Take antimalarial medications as prescribed', 'Cover your skin with clothing', 'Eliminate mosquito breeding sites']
    },
    'Jaundice': {
        'symptoms': ['Yellowing of the skin and eyes', 'Dark urine', 'Fatigue', 'Abdominal pain'],
        'precautions': ['Rest and get plenty of fluids', 'Avoid alcohol and certain medications', 'Eat a healthy diet', 'Treat underlying causes of jaundice']
    },
    'Impetigo': {
        'symptoms': ['Red sores that burst and develop honey-colored crusts', 'Itching', 'Rash', 'Swollen lymph nodes'],
        'precautions': ['Keep the affected area clean and dry', 'Avoid scratching or picking at the sores', 'Cover the sores with a bandage', 'Wash hands regularly']
    },
    'Hypothyroidism': {
        'symptoms': ['Fatigue', 'Weight gain', 'Dry skin', 'Depression'],
        'precautions': ['Take prescribed thyroid medication', 'Eat a balanced diet', 'Exercise regularly', 'Get regular check-ups']
    },
    'Hypoglycemia': {
        'symptoms': ['Shakiness', 'Sweating', 'Hunger', 'Confusion'],
        'precautions': ['Eat regular meals and snacks', 'Avoid skipping meals', 'Monitor blood sugar levels', 'Carry a source of fast-acting glucose']
    },
    'Hyperthyroidism': {
        'symptoms': ['Weight loss', 'Rapid heartbeat', 'Nervousness', 'Sweating'],
        'precautions': ['Take prescribed medications', 'Eat a balanced diet', 'Avoid excessive iodine intake', 'Manage stress levels']
    },
    'Hypertension': {
        'symptoms': ['High blood pressure', 'Headache', 'Chest pain', 'Shortness of breath'],
        'precautions': ['Adopt a healthy lifestyle with regular exercise and a balanced diet', 'Limit sodium intake', 'Manage stress levels', 'Take prescribed antihypertensive medications']
    },
    'Hepatitis E': {
        'symptoms': ['Fatigue', 'Jaundice', 'Nausea', 'Abdominal pain'],
        'precautions': ['Drink clean and purified water', 'Avoid eating raw or undercooked shellfish', 'Practice good personal hygiene', 'Get vaccinated if available']
    },
    'Hepatitis D': {
        'symptoms': ['Fatigue', 'Jaundice', 'Abdominal pain', 'Nausea'],
        'precautions': ['Get vaccinated against hepatitis B', 'Avoid alcohol and certain medications', 'Practice safe sex', 'Take precautions to prevent blood-to-blood contact']
    },
    'Hepatitis C': {
        'symptoms': ['Fatigue', 'Jaundice', 'Abdominal pain', 'Loss of appetite'],
        'precautions': ['Avoid sharing needles or other drug paraphernalia', 'Practice safe sex', 'Get vaccinated against hepatitis A and B', 'Follow proper infection control measures']
    },
    'Hepatitis B': {
        'symptoms': ['Fatigue', 'Jaundice', 'Abdominal pain', 'Loss of appetite'],
        'precautions': ['Get vaccinated against hepatitis B', 'Practice safe sex', 'Avoid sharing needles or other drug paraphernalia', 'Follow proper infection control measures']
    },
    'Hepatitis A': {
        'symptoms': ['Fatigue', 'Jaundice', 'Loss of appetite', 'Abdominal pain'],
        'precautions': ['Practice good hygiene, including handwashing', 'Drink clean and purified water', 'Avoid raw or undercooked shellfish', 'Get vaccinated if available']
    },
    'Heart attack': {
        'symptoms': ['Chest pain or discomfort', 'Shortness of breath', 'Nausea', 'Cold sweat'],
        'precautions': ['Call emergency services immediately', 'Chew and swallow aspirin if advised', 'Stay calm and try to keep breathing normally', 'Avoid any physical exertion']
    },
    'GERD': {
        'symptoms': ['Acid reflux', 'Heartburn', 'Regurgitation', 'Chest pain'],
        'precautions': ['Maintain a healthy weight', 'Avoid trigger foods and drinks', 'Eat smaller, more frequent meals', "Don't lie down immediately after eating"]
    },
    'Gastroenteritis': {
        'symptoms': ['Nausea', 'Vomiting', 'Diarrhea', 'Abdominal cramps'],
        'precautions': ['Stay hydrated with clear fluids', 'Gradually reintroduce bland foods', 'Practice good hand hygiene', 'Avoid preparing food for others']
    },
    'Fungal infection': {
        'symptoms': ['Itching', 'Redness', 'Rash', 'Peeling skin'],
        'precautions': ['Keep the affected area clean and dry', 'Avoid sharing personal items', 'Wear clean and breathable clothing', 'Use antifungal creams or powders']
    },
    'Drug Reaction': {
        'symptoms': ['Rash', 'Hives', 'Swelling', 'Breathing difficulties'],
        'precautions': ['Seek immediate medical attention', 'Discontinue the suspected medication', 'Keep a record of the reaction and inform healthcare providers', 'Avoid known triggers']
    },
    'Dimorphic hemorrhoids (piles)': {
        'symptoms': ['Painful bowel movements', 'Itching and irritation around the anus', 'Bleeding', 'Protrusion of lumps'],
        'precautions': ['Maintain good bowel habits', 'Avoid straining during bowel movements', 'Eat a high-fiber diet', 'Drink plenty of water']
    },
    'Diabetes': {
        'symptoms': ['Frequent urination', 'Excessive thirst', 'Unexplained weight loss', 'Fatigue'],
        'precautions': ['Monitor blood sugar levels regularly', 'Follow a balanced diet and portion control', 'Engage in regular physical activity', 'Take prescribed medications or insulin']
    },
    'Dengue': {
        'symptoms': ['High fever', 'Severe headache', 'Joint and muscle pain', 'Skin rash'],
        'precautions': ['Prevent mosquito breeding by eliminating stagnant water', 'Use mosquito nets or insect repellents', 'Wear protective clothing', 'Seek medical attention if symptoms worsen']
    },
    'Common Cold': {
        'symptoms': ['Runny or stuffy nose', 'Sneezing', 'Sore throat', 'Cough'],
        'precautions': ['Wash hands regularly', 'Cover your mouth and nose when coughing or sneezing', 'Avoid close contact with infected individuals', 'Stay hydrated and get plenty of rest']
    },
    'Chronic cholestasis': {
        'symptoms': ['Itching', 'Fatigue', 'Yellowing of the skin and eyes', 'Dark urine'],
        'precautions': ['Take prescribed medications', 'Eat a low-fat diet', 'Avoid alcohol and certain medications', 'Manage underlying liver conditions']
    },
    'Chickenpox': {
        'symptoms': ['Itchy rash with blisters', 'Fever', 'Fatigue', 'Headache'],
        'precautions': ['Avoid scratching the blisters', 'Keep the affected area clean and dry', 'Use over-the-counter medications for itching', 'Isolate the infected person to prevent spreading']
    },
    'Cervical spondylosis': {
        'symptoms': ['Neck pain', 'Stiffness', 'Headaches', 'Numbness or tingling in the arms'],
        'precautions': ['Practice good posture', 'Use a supportive pillow', 'Engage in neck and shoulder exercises', 'Apply heat or cold therapy']
    },
    'Bronchial Asthma': {
        'symptoms': ['Wheezing', 'Coughing', 'Shortness of breath', 'Chest tightness'],
        'precautions': ['Avoid triggers like allergens and irritants', 'Take prescribed asthma medications', 'Use inhalers correctly', 'Create an asthma action plan with your healthcare provider']
    },
    'Arthritis': {
        'symptoms': ['Joint pain', 'Swelling', 'Stiffness', 'Decreased range of motion'],
        'precautions': ['Engage in regular physical activity', 'Apply hot or cold packs to affected joints', 'Maintain a healthy weight', 'Use assistive devices if necessary']
    },
    'Allergy': {
        'symptoms': ['Sneezing', 'Runny or stuffy nose', 'Itchy or watery eyes', 'Rash or hives'],
        'precautions': ['Identify and avoid triggers', 'Keep windows closed to prevent allergens from entering', 'Use air purifiers or filters', 'Take prescribed antihistamines or allergy shots']
    },
    'Alcoholic hepatitis': {
        'symptoms': ['Abdominal pain', 'Jaundice', 'Fatigue', 'Loss of appetite'],
        'precautions': ['Stop consuming alcohol', 'Eat a healthy diet', 'Take prescribed medications', 'Seek support from healthcare professionals or support groups']
    },
    'AIDS': {
        'symptoms': ['Fatigue', 'Fever', 'Swollen lymph nodes', 'Weight loss'],
        'precautions': ['Practice safe sex', 'Use sterile needles for injections', 'Get tested regularly for HIV', 'Adhere to prescribed antiretroviral therapy']
    },
    'Acne': {
        'symptoms': ['Pimples', 'Blackheads', 'Whiteheads', 'Inflammation'],
        'precautions': ['Keep the skin clean', 'Avoid picking or squeezing pimples', 'Use non-comedogenic or oil-free skincare products', 'Manage stress levels']
    },
    '(vertigo) Paroymsal  Positional Vertigo': {
        'symptoms': ['Dizziness', 'Loss of balance', 'Nausea', 'Abnormal eye movements'],
        'precautions': ['Avoid sudden changes in head position', 'Use caution when getting up from lying down', 'Avoid bright lights and loud noises during episodes', 'Consult a healthcare provider for diagnosis and treatment']
    }
}

...
@register.filter
def get_name_id(s:str):
    return s.split("/")[-1].split(".")[0]
          

class EditPatientProfileView(UpdateView):
    model = User
    form_class = PatientProfileUpdateForm
    context_object_name = 'patient'
    template_name = 'accounts/patient/edit-profile.html'
    success_url = reverse_lazy('accounts:patient-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_patient)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Patient doesn't exists")
        return obj


class TakeAppointmentView(CreateView):
    template_name = 'appointment/take_appointment.html'
    form_class = TakeAppointmentForm
    extra_context = {
        'title': 'Take Appointment'
    }
    success_url = reverse_lazy('appointment:home')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'patient':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TakeAppointmentView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


"""
   For Doctor Profile
"""


class EditDoctorProfileView(UpdateView):
    model = User
    form_class = DoctorProfileUpdateForm
    context_object_name = 'doctor'
    template_name = 'accounts/doctor/edit-profile.html'
    success_url = reverse_lazy('accounts:doctor-profile-update')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_doctor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self, queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Patient doesn't exists")
        return obj


class AppointmentCreateView(CreateView):
    template_name = 'appointment/appointment_create.html'
    form_class = CreateAppointmentForm
    extra_context = {
        'title': 'Post New Appointment'
    }
    success_url = reverse_lazy('appointment:doctor-appointment')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'doctor':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(AppointmentCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment/appointment.html'
    context_object_name = 'appointment'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_doctor)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id).order_by('-id')


class PatientListView(ListView):
    model = TakeAppointment
    context_object_name = 'patients'
    template_name = "appointment/patient_list.html"

    def get_queryset(self):
        return self.model.objects.filter(appointment__user_id=self.request.user.id).order_by('-id')


class PatientDeleteView(DeleteView):
    model = TakeAppointment
    success_url = reverse_lazy('appointment:patient-list')


class AppointmentDeleteView(DeleteView):
    """
       For Delete any Appointment created by Doctor
    """
    model = Appointment
    success_url = reverse_lazy('appointment:doctor-appointment')


"""
   For both Profile
   
"""


class HomePageView(ListView):
    paginate_by = 9
    model = Appointment
    context_object_name = 'home'
    template_name = "home.html"

    def get_context(self):
        return self.model.objects.all().order_by('-id')


class ServiceView(TemplateView):
    template_name = 'appointment/service.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["images"] = ReportImages.objects.all()
        return context

class SearchView(ListView):
    paginate_by = 6
    model = Appointment
    template_name = 'appointment/search.html'
    context_object_name = 'appointment'

    def get_queryset(self):
        return self.model.objects.filter(location__contains=self.request.GET['location'],
                                         department__contains=self.request.GET['department'])
        

def analyze_report(request, filename):
    file = ReportImages.objects.filter(image='report/' + filename).first()
    
    if file:
        return HttpResponse(file.get_extracted_text())
    return HttpResponse("No file Found")

def check_disease(request):
    if request.method == "GET":
        return render(request, 'appointment/check_disease_home.html', context={
        'form' : SymptomsForm()
        })
    
    else:
        form = SymptomsForm(request.POST)
        input_for_analyze = ""
        result = None
        if form.is_valid():
            symptoms = form.cleaned_data.get('symptoms')
            for symp in symptoms[0:len(symptoms)-1]:
                input_for_analyze += symp + ","
            input_for_analyze += symptoms[-1]
        predicted_disease = predict_disease(input_for_analyze)
        final_result = defaultdict(dict)
        for i, j in predicted_disease.items():
            print(i)
            final_result[i] = {
                "disease_name" : i,
                "percentage" : j,
                "symptoms" : disease_dictionary.get(i).get('symptoms'),
                "precautions" : disease_dictionary.get(i).get('precautions')
            }
        return render(request, 'appointment/check_disease_response.html', context={
        'result' : final_result.values(),
        'symptoms' : input_for_analyze,
        })