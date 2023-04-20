import streamlit as st
import json
from datetime import datetime

# Globale Liste zur Speicherung des Verlaufs
history = []

def calculate_bmi(height, weight, gender):
    height_m = height / 100.0
    bmi = weight / (height_m ** 2)
    bmi_text = "Dein BMI beträgt {:.1f}".format(bmi)
    if bmi < 18.5:
        color = "red"
        status = "Untergewicht"
    elif bmi < 25:
        color = "green"
        status = "Normalgewicht"
    elif bmi < 30:
        color = "orange"
        status = "Übergewicht"
    else:
        color = "red"
        status = "Adipositas"
    bmi_text += " ({})".format(status)
    entry = {
        "date": datetime.now().strftime("%d.%m.%Y"),
        "height": height,
        "weight": weight,
        "bmi": bmi }
    
    history.append(entry)
    with open("data.json", "a") as f:
        f.write(json.dumps(entry) + "\n")
    return st.markdown("<h3 style='text-align:center;color:{};'>{}</h3>".format(color, bmi_text), unsafe_allow_html=True)

def show_bmi_calculator():
    st.title("BMI Rechner")
    # Eingabeaufforderungen für Datum, Größe, Gewicht und Geschlecht
    date = st.date_input("Wähle ein Datum")
    height = st.slider("Wähle deine Größe in cm", 120, 220, 170, 1)
    weight = st.slider("Wähle dein Gewicht in kg", 40, 150, 70, 1)
    gender = st.selectbox("Wähle dein Geschlecht", ["⚲ Gender", "♂ Männlich", "♀ Weiblich"])
    if gender == "♂ Männlich":
        gender_text = "männlich"
    elif gender == "♀ Weiblich":
        gender_text = "weiblich"
    else:
        gender_text = "⚲ Gender"
    st.write("Du hast am {} folgende Werte eingegeben: {} cm Größe, {} kg Gewicht als {}.".format(date.strftime("%d.%m.%Y"), height, weight, gender_text))
    if st.button("BMI berechnen"):
        calculate_bmi(height, weight, gender)
        
def show_history(history):
    if not history:
        # Wenn die Liste leer ist, gib eine Meldung aus
        st.write("Noch keine Einträge vorhanden.")
    else:
        for entry in history:
            st.write("- Datum: {}, Größe: {} cm, Gewicht: {} kg, BMI: {:.1f}".format(entry["date"], entry["height"], entry["weight"], entry["bmi"]))

def show_bmi_results():
    st.title("BMI Verlauf")
    with open("data.json", "r") as f:
        history = [json.loads(line) for line in f]
    show_history(history)

def show_bmi_interpretation():
    st.title("BMI Interpretationen")
    st.write("Bitte beachten Sie, dass ein BMI nur ein grober Indikator für den Körperzustand ist. Es bedeutet nicht unbedingt, dass Sie krank sind, wenn Sie einen niedrigen oder hohen BMI haben.")
    st.write("Der Body Mass Index (BMI) ist eine Möglichkeit, das Gewicht einer Person in Bezug auf ihre Größe zu bewerten.")
    st.write("Ein BMI von 18,5 oder weniger gilt als Untergewicht.")
    st.write("Ein BMI zwischen 18,5 und 24,9 gilt als normal.")
    st.write("Ein BMI zwischen 25 und 29,9 gilt als Übergewicht.")
    st.write("Ein BMI von 30 oder höher gilt als Adipositas.")
    st.write("Adipositas bedeutet, dass eine Person einen sehr hohen Körperfettanteil hat. Allerdings ist es dem BMI-Rechner nicht möglich, zwischen Fett- und Muskelmasse zu differenzieren.")

def show_bmi_general():
    st.title("Was ist ein BMI Rechner allgemein?")
    st.write("Der Body-Mass-Index (BMI) ist eine einfache Möglichkeit, das Verhältnis von Körpergewicht zu Körpergröße zu bestimmen. Es wird häufig als grober Indikator für den Körperzustand verwendet. Allerdings sollte man beachten, dass der BMI nicht immer ein zuverlässiger Indikator für die Körperzusammensetzung ist, da er nicht zwischen Fett- und Muskelmasse unterscheidet und somit Athleten oder muskulöse Menschen möglicherweise fälschlicherweise als übergewichtig eingestuft werden können. Auch spielt die Verteilung des Körperfetts auf die Gesundheit eine Rolle, so ist zum Beispiel das sogenannte Bauchfett besonders ungesund und mit einem erhöhten Risiko für Herz-Kreislauf-Erkrankungen und Diabetes verbunden.")

# Menü erstellen
menu = ["BMI Rechner", "BMI Verlauf", "BMI Interpretationen", "Was ist ein BMI Rechner allgemein?"]
choice = st.sidebar.selectbox("Wählen Sie eine Option", menu)

# Je nach Auswahl die entsprechende Funktion aufrufen
if choice == "BMI Rechner":
    show_bmi_calculator()
elif choice == "BMI Verlauf":
    show_bmi_results()
elif choice == "BMI Interpretationen":
    show_bmi_interpretation()
elif choice == "Was ist ein BMI Rechner allgemein?":
    show_bmi_general()
