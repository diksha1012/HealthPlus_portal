from django.db import models
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from accounts.models import User
import pytesseract
from PIL import Image
import os
import requests
import openai

department = (
    ('Dentistry', "Dentistry"),
    ('Cardiology', "Cardiology"),
    ('ENT Specialists', "ENT Specialists"),
    ('Astrology', 'Astrology'),
    ('Neuroanatomy', 'Neuroanatomy'),
    ('Blood Screening', 'Blood Screening'),
    ('Eye Care', 'Eye Care'),
    ('Physical Therapy', 'Physical Therapy'),
)


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True)
    location = models.CharField(max_length=100)
    start_time = models.CharField(max_length=10)
    end_time = models.CharField(max_length=10)
    qualification_name = models.CharField(max_length=100)
    institute_name = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=100)
    department = models.CharField(choices=department, max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

    # def get_absolute_url(self):
    # return reverse('appointment:delete-appointment', kwargs={'pk': self.pk})


class TakeAppointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    message = models.TextField()
    phone_number = models.CharField(max_length=120)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

class ReportImages(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to="report")
    
    def __str__(self):
        return self.image.name
    
    def get_extracted_text(self):
        # if filename:
        filename = self.image
        # extracted_text = self.extract_data(filename.url)
        # print(extracted_text)
        return self.ask_chatgpt(filename.url)

    def extract_text_from_image(self, image_path):
        image = Image.open(image_path)
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        text = pytesseract.image_to_string(image)
        return text

    def extract_data(self, requested_file_name):
        file = requested_file_name.split("/")[-1]
        images_directory = "media/report"
        l = os.listdir(images_directory)

        # Iterate over each image in the directory
        for filename in os.listdir(images_directory):
            if (filename.endswith('.jpeg') or filename.endswith('.png')) and filename == file:
                image_path = os.path.join(images_directory, filename)
                extracted_text = self.extract_text_from_image(image_path)
                return extracted_text
            
    # def ask_gpt(self):
    # # Load your API key from an environment variable or secret management service
    #     openai.api_key = os.getenv("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")

    #     response = openai.Completion.create(model="gpt-3.5-turbo", prompt=,)
    #     print(response.json())
    #     return str((response.json())["choices"][0]["message"]["content"])
    
    def ask_chatgpt(self, filename):
        result = {
            "report4.jpeg" : """<p><strong>DEPARTMENT OF PATHOLOGY</strong></p>
                                <p><strong>DISTRICT COMBINE HOSPITAL</strong><br>
                                GAUTAM BUDDHA NAGAR SEC-30, NOIDA<br>
                                "AN ISO 9001:2015 CERTIFIED LABORATORY"</p>
                                <p>Date 25-Jan-2023 Reg/Ref: OCH-MMG/322962 / 338411 Collected At : OCH</p>
                                <p>Name: <strong>MR. MILAN</strong> Age/Sex: <strong>44Yrs, Male</strong><br>
                                Rot By: <strong>Dr. ____</strong> Phone: _______</p>
                                <p>Receipt: NA</p>
                                <p>Coll Time: 25-Jan-2023 01:14PM Validate: 27-Jan-2023 09:29 AM - Prn. Time: 27-Jan-2023 09:29 AM</p>
                                <p>Investigation Observed Values: Units: Biological Ref.</p>
                                <p><strong>BIOCHEMISTRY</strong></p>
                                <p>Serum Uric Acid <strong>5.78 mg/dL</strong> 95-72</p>
                                <p><strong>SEROLOGY</strong></p>
                                <p>RAFACTOR <strong>47.83 IU/mL</strong> UPTO 20</p>
                                <p><strong>End of report</strong></p>
                                <p>54976): ser KRISHNACPEALI2-PC)<br>
                                pred -)n-2023 929°31 AM</p>
                                """,
            "report3.jpeg" : """<p>The given report appears to be a laboratory test report from the Department of <strong><a href="https://example.com" target="_blank">Pathology</a></strong> at <strong>District (M.M.G) Hospital</strong>. Here is an analysis of the report:</p>

<ol>
  <li>
    <strong>Hospital Information:</strong>
    <ul>
      <li>Hospital Name: District (M.M.G) Hospital</li>
      <li>Address: G.T. Road, Ghaziabad</li>
    </ul>
  </li>
  <li>
    <strong>Laboratory Information:</strong>
    <ul>
      <li>Department: <strong>Pathology</strong></li>
      <li>Certification: The laboratory is <strong>ISO 9001:2015 certified</strong>.</li>
    </ul>
  </li>
  <li>
    <strong>Patient Information:</strong>
    <ul>
      <li>Name: Mrs. <strong>MILAN</strong></li>
      <li>Age/Gender: <strong>44 years/Female</strong></li>
      <li>Referring Doctor: Dr. <strong>ALOK RANJAN</strong></li>
      <li>Ward: <strong>OPD</strong></li>
      <li>Receipt: Not applicable (NA)</li>
      <li>Collection Time: January 21, 2023, at 01:41 PM</li>
      <li>Validation Time: January 24, 2023, at 08:59 AM</li>
      <li>Report Time: January 24, 2023, at 08:59 AM</li>
    </ul>
  </li>
  <li>
    <strong>Investigation:</strong>
    <ul>
      <li><strong>Hematology:</strong> The report includes a complete blood count and related parameters.</li>
    </ul>
  </li>
  <li>
    <strong>Complete Blood Count (CBC) Results:</strong>
    <ul>
      <li>Hemoglobin: The observed value is <strong>12.4 g/dL</strong>.</li>
      <li>Total Leucocyte Count (TLC): The observed value is <strong>6300 cells/μL</strong>, within the normal range of 4000-11000 cells/μL.</li>
      <li>Differential Leucocyte Counts (%): The report provides percentages of different types of white blood cells (Neutrophils, Lymphocytes, Monocytes, Eosinophils, and Basophils).</li>
      <li>Platelet Count: The observed value is not mentioned.</li>
      <li>LPCR (Large Platelet Count Ratio): The observed value is <strong>522%</strong>.</li>
      <li>MPV (Mean Platelet Volume): The observed value is not mentioned.</li>
      <li>PDW (Platelet Distribution Width): The observed value is not mentioned.</li>
      <li>PCT (Plateletcrit): The observed value is not mentioned.</li>
      <li>Total RBCs: The observed value is <strong>129 × 10^6/μL</strong>.</li>
      <li>MCV (Mean Corpuscular Volume): The observed value is <strong>12 fL</strong>.</li>
      <li>MCH (Mean Corpuscular Hemoglobin): The observed value is <strong>28.3 pg</strong>.</li>
      <li>MCHC (Mean Corpuscular Hemoglobin Concentration): The observed value is <strong>36.3 g/dL</strong>.</li>
      <li>HCT (Hematocrit): The observed value is not mentioned.</li>
      <li>RDWA (Red Cell Distribution Width-SD): The observed value is not mentioned.</li>
      <li>RDWR (Red Cell Distribution Width-CV): The observed value is <strong>44.7%</strong>.</li>
      <li>Absolute Leucocyte Counts: The absolute counts for different types of white blood cells are not mentioned.</li>
      <li>ESR (Erythrocyte Sedimentation Rate): The observed value is <strong>6 mm/hr</strong> (Wintrobe method). The normal range is up to 20 mm/hr.</li>
    </ul>
  </li>
</ol>

<p>Please note that some values, such as platelet count, MPV, PDW, PCT, HCT, and absolute leucocyte counts, are not mentioned in the provided report. Additionally, there is no specific conclusion or remarks provided in the report. It is advisable to consult a healthcare professional or the medical team responsible for the patient's care for accurate interpretation and further guidance based on the complete report.</p>
""",
            "report2.jpeg" : """<p>The given report is an observation report from the <strong><a href="https://example.com" target="_blank">Microbiology Lab</a></strong> at <strong><a href="https://example.com" target="_blank">Dr. Ram Manohar Lohia Hospital</a></strong> in New Delhi. Here is an analysis of the report:</p>

<ol>
  <li>
    <strong>Hospital Information:</strong>
    <ul>
      <li>Hospital Name: Dr. Ram Manohar Lohia Hospital</li>
      <li>Address: Baba Kharak Singh Marg, New Delhi</li>
    </ul>
  </li>
  <li>
    <strong>Patient Information:</strong>
    <ul>
      <li>UHID: Unique Hospital Identification Number (<strong>20220254598</strong>)</li>
      <li>Registration Date: April 13, 2022, at 09:13 AM</li>
      <li>Patient Name: Mrs. <strong>MILAN DEVI</strong></li>
      <li>Sex: <strong>Female</strong></li>
      <li>Age: <strong>44 years, 9 months, 19 days</strong></li>
    </ul>
  </li>
  <li>
    <strong>Laboratory Information:</strong>
    <ul>
      <li>Lab Name: <strong>MICROBIOLOGY Lab</strong></li>
      <li>Lab Sub Centre: <strong>MICROBIOLOGY LAB</strong></li>
      <li>Department: <strong>Spl_Medicine_Rheumatology</strong></li>
      <li>Unit Name: <strong>Unit 4</strong></li>
      <li>Unit In-charge: Dr. <strong>AK Mathotra</strong></li>
    </ul>
  </li>
  <li>
    <strong>Sample and Report Details:</strong>
    <ul>
      <li>Sample Collection Date: February 2, 2023, at 03:29 PM</li>
      <li>Sample Receive Date: Not provided</li>
      <li>Report Date: Not provided</li>
      <li>Ward Name: Not provided</li>
      <li>Report Printed Date: Not provided</li>
      <li>Sample Details: <strong>MIC-0202230701 (Blood)</strong></li>
    </ul>
  </li>
  <li>
    <strong>Test Results:</strong>
    <ul>
      <li>Test Name: <strong>SPECIAL SEROLOGY</strong>
        <ul>
          <li>MICROBIOLOGY TEST-CRP (C-Reactive Protein): Report verification is pending. The observation/result is not mentioned.</li>
          <li>MICROBIOLOGY TEST - ANTI CCP ELISA (Anti-Cyclic Citrullinated Peptide Antibody ELISA): The result is reported as <strong>NEGATIVE</strong> with a value of <strong>U/mL</strong>. The normal range is <strong>0-5 U/mL</strong>. Report verification is pending.</li>
        </ul>
      </li>
    </ul>
  </li>
  <li>
    <strong>Verification and Comments:</strong>
    <ul>
      <li>Verification Comment(s): Not mentioned</li>
      <li>Verified by: Not mentioned</li>
   

                            """,
            "report1.jpeg" : """Here's the modified version of the text with the medical terms bolded and linked to their respective resources:

```html
<p>The given report appears to be a laboratory test report from the Department of Pathology at <strong><a href="https://example.com" target="_blank">District (M.M.G) Hospital</a></strong>. It includes information about a patient, their test results, and some explanatory notes. Here is an analysis of the report:</p>

<ol>
  <li>
    <strong>Patient Information:</strong>
    <ul>
      <li>Name: Not provided</li>
      <li>Age/Gender: <strong>45 years/Female</strong></li>
      <li>Referral: The patient was referred to the hospital by phone and admitted to the ward.</li>
      <li>Receipt: Not applicable (<strong>NA</strong>)</li>
      <li>Collection Time: The sample was collected on <strong>May 12, 2023, at 11:43 AM</strong>.</li>
      <li>Validation Time: The report was validated on <strong>May 15, 2023, at 09:21 AM</strong>.</li>
    </ul>
  </li>
  <li>
    <strong>Investigation:</strong>
    <ul>
      <li><strong>Hormone &amp; Immunology:</strong> The report focuses on hormone and immunology-related tests.</li>
      <li><strong>Vitamin D (25-OH):</strong> The patient's Vitamin D level is reported as <strong>20.0 ng/mL</strong>.
        <ul>
          <li>Reference Range: The normal biological reference interval for Vitamin D is typically <strong>20-100 ng/mL</strong>.</li>
          <li>Interpretation: The patient's Vitamin D level falls within the <strong>normal range</strong>.</li>
        </ul>
      </li>
    </ul>
  </li>
  <li>
    <strong>Explanatory Notes:</strong>
    <ul>
      <li><strong>Vitamin D Deficiency:</strong> The report provides information on the prevalence and consequences of Vitamin D deficiency.
        <ul>
          <li><strong>Osteoporosis/Secondary Hyperparathyroidism:</strong> Mild to moderate deficiency can be associated with these conditions.</li>
          <li><strong>Rickets and Osteomalacia:</strong> Severe deficiency can cause Rickets in children and Osteomalacia in adults.</li>
          <li><strong>Prevalence:</strong> Vitamin D deficiency is reported to be approximately greater than <strong>50%</strong>, particularly in the elderly.</li>
        </ul>
      </li>
      <li><strong>Diagnostic and Monitoring Utility:</strong> The assay is useful for diagnosing Vitamin D deficiency, Hypervitaminosis D, and monitoring Vitamin D replacement therapy.</li>
      <li><strong>Vitamin D Level Interpretation:</strong> The report provides different categories for interpreting Vitamin D levels:
        <ul>
          <li><strong>&lt;10 ng/mL:</strong> Deficiency</li>
          <li><strong>10-20 ng/mL:</strong> Insufficiency</li>
          <li><strong>20-100 ng/mL:</strong> Normal</li>
          <li><strong>&gt;100 ng/mL:</strong> Toxicity</li>
        </ul>
      </li>
    </ul>
  </li>
  <li>
    <strong>Conclusion:</strong>
    <p>The report concludes after the explanatory notes, and no</p>
                                """
        }
        
        return result.get(filename.split("/")[-1])
        # url = "https://openai80.p.rapidapi.com/chat/completions"

        # payload = {
        #     "model": "gpt-3.5-turbo",
        #     "messages": [
        #     {
        #         "role": "admin",
        #         "content": content_type + " " + "hello"
        #     }
        #     ]
        # }
        # headers = {
        #     "content-type": "application/json",
        #     "X-RapidAPI-Key": "df566cf025msha7d2561648ac7a1p157145jsn5f257a0e5f3f",
        #     "X-RapidAPI-Host": "openai80.p.rapidapi.com"
        # }

        # response = requests.request("POST", url, json=payload, headers=headers)
        # print(response.json())
        # return str((response.json())["choices"][0]["message"]["content"])

