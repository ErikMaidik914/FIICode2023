# FIICode2023: Team MedEase
### Members: Calin Andrei, Erik Maidik, David Seu
## moto:"Making healthcare accessible to all"

## ![logo](https://user-images.githubusercontent.com/115073797/228282178-b3dd99ae-5781-4804-8fcf-6c901688d9ba.jpg)
### Presentation video: https://youtu.be/ckYANJDRGcw

Welcome to our medical application: MedEase !!!
 
This project was meant to improve the work of each patient, but also make consultation scheduling for doctors
a lot easier, containing also some **EXTRA** user-friendly features such as the option for patients to give a rating from 1 to 5 and the option to upload a profile picture both as a patient and as a doctor
to their doctor or the schedule of the doctor being present on top of the patient's calendar for a better functioning of the community, 
the option to specify the lifestyle of the patient, if he is a smoker, drinker, has any allergies that 
might be worth mentioning before taking a certain type of medication.
Our application is also operating with a database that is set to generate a bunch of doctors, patients, allergies and so on in order for 
us to check the functionalities at any given time.
Besides that, the app meets every requirement from the given pdf: you cand add infinetly pdf in a consultation as a doctor and they will all be merged in on so both the patient and the doctor can see it, to register as a doctor you must provive a valid pdf(meaning that it has to contain the full name that is in the register form along with the words "University" and "Medical Degree"> Another intersting feature that it has is that it gets the doctors nearby a pacient using geolocation, meaning it caluclates the distance between the location of the doctor and the patient using coordintates in real world. Further on it has an interesting and minimalistic design,it is mostly responsive 
and the color theme white+purple is used on almost each page.
Another aspect to be mentioned is that the sms functionality only works (for now) for numbers that are verified by the app "Twilio", 
as you need to pay for a subscription in order for it to work on every number possible.(thankfully we happen to have access to the one present in the video).

The application is build on the Flask framework and uses techologies such as geolocation, pdf extraction tools, databases 
