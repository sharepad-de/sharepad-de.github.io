# -*- coding: utf-8 -*-
"""Generate the AVV (Auftragsverarbeitungsvertrag) PDF with fillable form fields."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, PageBreak, KeepTogether, Flowable,
)
from reportlab.pdfbase import pdfform
from reportlab.pdfgen import canvas

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "static", "Auftragsverarbeitungsvertrag.pdf")

# ---------- styles ----------
styles = getSampleStyleSheet()
body = ParagraphStyle(
    "body", parent=styles["BodyText"],
    fontName="Helvetica", fontSize=9.5, leading=13,
    alignment=TA_JUSTIFY, spaceAfter=4,
)
h1 = ParagraphStyle(
    "h1", parent=styles["Heading1"],
    fontName="Helvetica-Bold", fontSize=15, leading=19,
    spaceBefore=4, spaceAfter=8, textColor=colors.HexColor("#2a2a2a"),
)
h2 = ParagraphStyle(
    "h2", parent=styles["Heading2"],
    fontName="Helvetica-Bold", fontSize=11, leading=14,
    spaceBefore=10, spaceAfter=4, textColor=colors.HexColor("#2a2a2a"),
)
h3 = ParagraphStyle(
    "h3", parent=styles["Heading3"],
    fontName="Helvetica-Bold", fontSize=10, leading=13,
    spaceBefore=6, spaceAfter=2,
)
small = ParagraphStyle(
    "small", parent=body, fontSize=8.5, leading=11,
)
centered = ParagraphStyle(
    "centered", parent=body, alignment=TA_CENTER,
)

# ---------- form fields as flowables ----------
class FormField(Flowable):
    def __init__(self, name, width, height=0.6*cm, tooltip="", maxlen=200,
                 multiline=False, value=""):
        Flowable.__init__(self)
        self.name = name
        self.width = width
        self.height = height
        self.tooltip = tooltip or name
        self.maxlen = maxlen
        self.multiline = multiline
        self.value = value

    def wrap(self, *args):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.acroForm.textfield(
            name=self.name,
            tooltip=self.tooltip,
            x=0, y=0,
            width=self.width, height=self.height,
            borderStyle="underlined",
            borderColor=colors.HexColor("#888888"),
            fillColor=colors.HexColor("#f5f0e8"),
            textColor=colors.black,
            forceBorder=True,
            fontName="Helvetica",
            fontSize=9.5,
            maxlen=self.maxlen,
            fieldFlags="multiline" if self.multiline else "",
            value=self.value,
        )

class SignatureLine(Flowable):
    """A labeled signature line with a date field and a location field."""
    def __init__(self, name_prefix, label, width=8.5*cm):
        Flowable.__init__(self)
        self.name_prefix = name_prefix
        self.label = label
        self.width = width
        self.height = 3.8*cm

    def wrap(self, *args):
        return self.width, self.height

    def draw(self):
        c = self.canv
        # date / location fields on top
        c.setFont("Helvetica", 8.5)
        c.drawString(0, self.height - 0.3*cm, "Ort, Datum:")
        c.acroForm.textfield(
            name=self.name_prefix + "_ort_datum",
            tooltip="Ort und Datum",
            x=1.9*cm, y=self.height - 0.55*cm,
            width=self.width - 1.9*cm, height=0.55*cm,
            borderStyle="underlined",
            borderColor=colors.HexColor("#888888"),
            fillColor=colors.HexColor("#f5f0e8"),
            forceBorder=True, fontName="Helvetica", fontSize=9.5,
        )
        # signature area (blank box for ink signature)
        sig_y = self.height - 2.6*cm
        c.setFillColor(colors.HexColor("#f5f0e8"))
        c.setStrokeColor(colors.HexColor("#888888"))
        c.rect(0, sig_y, self.width, 1.6*cm, stroke=1, fill=1)
        c.setFillColor(colors.black)
        # label underneath
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(0, sig_y - 0.35*cm, "Unterschrift / Stempel")
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0, sig_y - 0.75*cm, self.label)


def hr(width=None):
    from reportlab.platypus import HRFlowable
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#bbbbbb"),
                      spaceBefore=4, spaceAfter=4)


# ---------- content ----------
story = []

def P(t): story.append(Paragraph(t, body))
def H1(t): story.append(Paragraph(t, h1))
def H2(t): story.append(Paragraph(t, h2))
def H3(t): story.append(Paragraph(t, h3))
def S(h=0.2*cm): story.append(Spacer(1, h))

# --- Title ---
H1("Auftragsverarbeitungsvertrag (AVV)")
story.append(Paragraph("gemäß Art. 28 DSGVO zum Dienst <b>sharePAD</b>", body))
S(0.4*cm)

# --- Parties ---
H2("Zwischen den Parteien")

P("<b>Verantwortlicher</b> (nachfolgend „Kundenorganisation“) – vom Kunden auszufüllen:")
tbl_data = [
    ["Name der Organisation:", FormField("verant_name", 11*cm, tooltip="Vollständiger Name der Organisation")],
    ["Anschrift:", FormField("verant_anschrift", 11*cm, tooltip="Straße, PLZ, Ort, Land")],
    ["Vertreten durch:", FormField("verant_vertreter", 11*cm, tooltip="Name und Funktion der vertretungsberechtigten Person")],
    ["E-Mail:", FormField("verant_email", 11*cm, tooltip="E-Mail-Adresse für datenschutzrechtliche Kommunikation")],
    ["Registernummer (falls vorhanden):", FormField("verant_register", 11*cm, tooltip="z. B. Vereinsregister, Handelsregister")],
]
t = Table(tbl_data, colWidths=[5*cm, 11.5*cm])
t.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("FONTNAME", (0,0), (0,-1), "Helvetica"),
    ("FONTSIZE", (0,0), (-1,-1), 9.5),
    ("TOPPADDING", (0,0), (-1,-1), 2),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))
story.append(t)
S(0.3*cm)

P("<b>und</b>")
S(0.15*cm)
P("<b>Auftragsverarbeiter</b> (nachfolgend „sharePAD-Betreiber“):")
P("Robert Hölzl Cloud Platforms<br/>"
  "Traunsteinerstr. 44<br/>"
  "83093 Bad Endorf<br/>"
  "Deutschland<br/>"
  "E-Mail: robert.hoelzl@sharepad.de")
S(0.25*cm)
P("wird der folgende Vertrag über die Verarbeitung personenbezogener Daten im Auftrag "
  "(nachfolgend „Vertrag“ oder „AVV“) geschlossen. Er konkretisiert die Pflichten "
  "der Parteien zum Datenschutz, die sich aus dem zwischen ihnen bestehenden Hauptvertrag "
  "über die Nutzung des Dienstes sharePAD (nachfolgend „Hauptvertrag“) ergeben.")

# --- § 1 ---
H2("§ 1 Gegenstand, Art und Zweck der Verarbeitung")
P("(1) Gegenstand des Auftrags ist die Verarbeitung personenbezogener Daten durch den "
  "sharePAD-Betreiber für die Kundenorganisation im Rahmen der Bereitstellung des "
  "Internetdienstes sharePAD (abrufbar unter app.sharepad.de bzw. beta.sharepad.de).")
P("(2) sharePAD ermöglicht Organisationen, gemeinschaftlich genutzte Ressourcen "
  "(z. B. Fahrzeuge) unter ihren Mitgliedern zu verwalten und zu reservieren. Die "
  "Verarbeitung umfasst insbesondere das Anlegen, Bearbeiten und Löschen von "
  "Mitgliedsdaten und Reservierungen, die Authentifizierung der Nutzer, den Versand "
  "transaktionaler E-Mails, die Abrechnung sowie unterstützende Funktionen wie "
  "Geocoding und Bildverarbeitung.")
P("(3) Art der Verarbeitung: Erheben, Erfassen, Speichern, Verändern, Auslesen, "
  "Abfragen, Verwenden, Offenlegen durch Übermittlung, Abgleichen, Einschränken, "
  "Löschen und Vernichten personenbezogener Daten mittels automatisierter Verfahren.")
P("(4) Zweck der Verarbeitung ist ausschließlich die vertragsgemäße Erbringung der "
  "Leistungen nach dem Hauptvertrag. Eine Verarbeitung zu eigenen Zwecken des "
  "sharePAD-Betreibers findet – außerhalb der gesetzlich erlaubten Ausnahmen – "
  "nicht statt.")

# --- § 2 ---
H2("§ 2 Dauer des Auftrags")
P("Die Laufzeit dieses Vertrags entspricht der Laufzeit des Hauptvertrags. Er endet "
  "automatisch mit dessen Beendigung, ohne dass es einer gesonderten Kündigung "
  "bedarf. Die Pflichten aus § 10 (Löschung und Rückgabe) sowie aus datenschutz- "
  "und handelsrechtlichen Aufbewahrungsvorschriften bleiben hiervon unberührt.")

# --- § 3 ---
H2("§ 3 Art der personenbezogenen Daten und Kategorien betroffener Personen")
H3("(1) Kategorien betroffener Personen")
P("Mitglieder der Kundenorganisation (einschließlich Mitgliedern mit administrativen "
  "Rollen sowie Supervisor-Rollen), gegebenenfalls Mitglieder von Partner-"
  "Organisationen, an die einzelne Ressourcen freigegeben wurden.")
H3("(2) Kategorien personenbezogener Daten")
P("• <b>Stammdaten:</b> Vor- und Nachname, E-Mail-Adresse, Telefonnummer, "
  "Postanschrift, Mitgliedsnummer, Rolle innerhalb der Organisation, "
  "Datum einer Beendigung der Mitgliedschaft.")
P("• <b>Authentifizierungsdaten:</b> Passwort-Hashes (bcrypt), Sitzungs-Token (JWT) "
  "im Browser des Mitglieds, ggf. API-Schlüssel (SHA-256-Hash).")
P("• <b>Reservierungsdaten:</b> Reservierungen mit Zeitraum, Kommentar und Bezug "
  "zum reservierenden Mitglied sowie vollständige Änderungshistorie (Audit-Log).")
P("• <b>Technische Daten:</b> Server-Logs (IP-Adresse, Zeitstempel, aufgerufener "
  "Pfad, HTTP-Statuscode) sowie Fehler- und Performance-Ereignisse ohne "
  "personenbezogene Zusatzinformationen.")
P("• <b>Organisationsdaten:</b> Name, Anschrift, Geokoordinaten, Logo sowie "
  "Vertrags- und Abrechnungsstatus der Kundenorganisation.")

# --- § 4 ---
H2("§ 4 Pflichten des sharePAD-Betreibers")
P("(1) Der sharePAD-Betreiber verarbeitet personenbezogene Daten ausschließlich "
  "im Rahmen des Hauptvertrags, dieses AVV und auf dokumentierte Weisung der "
  "Kundenorganisation. Dies gilt auch für die Übermittlung in Drittländer. Ist er "
  "durch das Recht der Union oder eines Mitgliedstaats zu einer weitergehenden "
  "Verarbeitung verpflichtet, teilt er der Kundenorganisation diese rechtlichen "
  "Anforderungen vor der Verarbeitung mit, sofern das betreffende Recht eine "
  "solche Mitteilung nicht wegen eines wichtigen öffentlichen Interesses verbietet.")
P("(2) Der sharePAD-Betreiber gewährleistet, dass die zur Verarbeitung befugten "
  "Personen zur Vertraulichkeit verpflichtet sind oder einer angemessenen "
  "gesetzlichen Verschwiegenheitspflicht unterliegen.")
P("(3) Er trifft die nach Art. 32 DSGVO erforderlichen technischen und "
  "organisatorischen Maßnahmen (TOMs), die in Anlage 2 beschrieben sind. Eine "
  "Anpassung der TOMs an den Stand der Technik bleibt dem sharePAD-Betreiber "
  "vorbehalten, soweit das Schutzniveau nicht unterschritten wird.")
P("(4) Er unterstützt die Kundenorganisation im Rahmen des technisch Möglichen und "
  "Zumutbaren bei der Beantwortung von Anträgen betroffener Personen (Art. 12–23 "
  "DSGVO), bei der Sicherstellung der Datensicherheit (Art. 32 DSGVO), bei der "
  "Meldung von Datenschutzverletzungen (Art. 33, 34 DSGVO) sowie bei "
  "Datenschutz-Folgenabschätzungen (Art. 35, 36 DSGVO).")
P("(5) Er meldet der Kundenorganisation Verletzungen des Schutzes personenbezogener "
  "Daten unverzüglich, spätestens innerhalb von 72 Stunden nach Kenntnisnahme, "
  "per E-Mail an die in der Präambel angegebene Adresse. Die Meldung enthält die "
  "nach Art. 33 Abs. 3 DSGVO erforderlichen Angaben, soweit sie verfügbar sind.")
P("(6) Er stellt der Kundenorganisation auf Anforderung die zum Nachweis der "
  "Einhaltung der Pflichten aus Art. 28 DSGVO erforderlichen Informationen zur "
  "Verfügung.")
P("(7) Er informiert die Kundenorganisation unverzüglich, wenn er der Auffassung "
  "ist, dass eine Weisung gegen datenschutzrechtliche Vorschriften verstößt.")

# --- § 5 ---
H2("§ 5 Weisungsrecht der Kundenorganisation")
P("(1) Die Kundenorganisation ist im Rahmen dieses Vertrags allein für die "
  "Rechtmäßigkeit der Verarbeitung und für die Wahrung der Betroffenenrechte "
  "verantwortlich.")
P("(2) Weisungen erfolgen grundsätzlich in Textform (E-Mail genügt). Regelmäßige "
  "Bedienhandlungen innerhalb der Benutzeroberfläche von sharePAD (z. B. Anlegen, "
  "Ändern oder Löschen von Mitgliedern, Ressourcen und Reservierungen) gelten als "
  "vereinbarungsgemäße Einzelweisungen.")
P("(3) Mündliche Weisungen sind unverzüglich in Textform zu bestätigen.")

# --- § 6 ---
H2("§ 6 Sub-Auftragsverarbeiter")
P("(1) Die Kundenorganisation erteilt dem sharePAD-Betreiber die allgemeine "
  "schriftliche Genehmigung zum Einsatz der in <b>Anlage 1</b> benannten "
  "Sub-Auftragsverarbeiter.")
P("(2) Der sharePAD-Betreiber ist berechtigt, weitere Sub-Auftragsverarbeiter "
  "hinzuzuziehen oder bestehende zu ersetzen. Er informiert die Kundenorganisation "
  "hierüber mindestens 14 Tage im Voraus in Textform unter Angabe von Name, "
  "Anschrift, Sitzland und Zweck der Beauftragung. Die Information erfolgt an die "
  "oben angegebene E-Mail-Adresse der Kundenorganisation oder durch Hinweis in der "
  "Administrationsoberfläche von sharePAD.")
P("(3) Die Kundenorganisation kann einer Änderung aus wichtigem datenschutz­"
  "rechtlichem Grund innerhalb der Ankündigungsfrist in Textform widersprechen. "
  "Kommt keine Einigung zustande, sind beide Parteien berechtigt, den Hauptvertrag "
  "mit einer Frist von einem Monat zum Monatsende zu kündigen.")
P("(4) Der sharePAD-Betreiber verpflichtet seine Sub-Auftragsverarbeiter "
  "vertraglich zu datenschutzrechtlichen Pflichten, die denen dieses Vertrags "
  "entsprechen, insbesondere zur Einhaltung hinreichender TOMs.")

# --- § 7 ---
H2("§ 7 Drittlandtransfers")
P("Eine Übermittlung personenbezogener Daten in ein Drittland außerhalb der EU/"
  "des EWR findet nur statt, soweit die Voraussetzungen der Art. 44 ff. DSGVO "
  "erfüllt sind (insbesondere Angemessenheitsbeschluss oder Standardvertrags­"
  "klauseln). Aktuell betrifft dies die Übermittlung von Adressdaten und "
  "Geokoordinaten an Mapbox, Inc. (USA); Grundlage ist der Angemessenheits­"
  "beschluss zum EU-US Data Privacy Framework bzw. ergänzend Standardvertrags­"
  "klauseln (Art. 46 Abs. 2 lit. c DSGVO). Weitere Einzelheiten sind in "
  "Anlage 1 aufgeführt.")

# --- § 8 ---
H2("§ 8 Kontroll- und Nachweisrechte")
P("(1) Der sharePAD-Betreiber weist die Einhaltung der in diesem Vertrag "
  "niedergelegten Pflichten in geeigneter Weise nach, insbesondere durch "
  "aktuelle Dokumentation der TOMs, Selbstauskünfte oder – soweit vorhanden – "
  "Zertifikate, Testate oder Berichte unabhängiger Prüfstellen.")
P("(2) Die Kundenorganisation ist berechtigt, nach vorheriger Anmeldung mit "
  "angemessener Vorlaufzeit (mindestens 30 Tage) während der üblichen "
  "Geschäftszeiten ohne Störung des Betriebsablaufs Kontrollen durchzuführen oder "
  "durch einen benannten Prüfer durchführen zu lassen. Der Prüfer darf kein "
  "Wettbewerber des sharePAD-Betreibers sein und ist zur Vertraulichkeit "
  "verpflichtet.")
P("(3) Der sharePAD-Betreiber kann für den Mehraufwand einer solchen Prüfung "
  "ein angemessenes Entgelt nach seinem jeweils gültigen Stundensatz verlangen, "
  "sofern die Prüfung nicht aus einem konkreten Anlass (z. B. nach einer "
  "Datenpanne) erfolgt.")

# --- § 9 ---
H2("§ 9 Haftung")
P("Für die Haftung der Parteien gelten Art. 82 DSGVO sowie die Regelungen des "
  "Hauptvertrags. Eine Haftungsbegrenzung im Hauptvertrag gilt auch für Ansprüche "
  "aus diesem AVV, soweit zwingendes Recht nicht entgegensteht.")

# --- § 10 ---
H2("§ 10 Löschung und Rückgabe nach Beendigung")
P("(1) Nach Beendigung des Hauptvertrags hat der sharePAD-Betreiber nach Wahl der "
  "Kundenorganisation alle personenbezogenen Daten zu löschen oder an die "
  "Kundenorganisation in einem strukturierten, gängigen und maschinenlesbaren "
  "Format zurückzugeben, sofern nicht eine gesetzliche Pflicht zur Speicherung "
  "besteht.")
P("(2) Bestehende gesetzliche Aufbewahrungspflichten (insbesondere handels- und "
  "steuerrechtliche Fristen nach § 147 AO und § 257 HGB) bleiben hiervon "
  "unberührt.")
P("(3) Reservierungsdaten, die gemäß der Datenschutzerklärung nach Ablauf "
  "definierter Fristen anonymisiert werden, verbleiben in anonymisierter Form zu "
  "statistischen Zwecken beim sharePAD-Betreiber, soweit kein Personenbezug mehr "
  "besteht.")

# --- § 11 ---
H2("§ 11 Schlussbestimmungen")
P("(1) Im Konfliktfall zwischen den Regelungen dieses AVV und des Hauptvertrags "
  "gehen die Regelungen dieses AVV vor. Im Konfliktfall zwischen diesem AVV und "
  "den jeweils aktuell geltenden datenschutzrechtlichen Vorschriften geht "
  "letzteres vor.")
P("(2) Änderungen und Ergänzungen dieses Vertrags bedürfen der Textform.")
P("(3) Es gilt deutsches Recht unter Ausschluss des UN-Kaufrechts.")
P("(4) Ausschließlicher Gerichtsstand ist Rosenheim, soweit die Kundenorganisation "
  "Kaufmann, juristische Person des öffentlichen Rechts oder öffentlich-rechtliches "
  "Sondervermögen ist.")
P("(5) Sollte eine Bestimmung dieses Vertrags unwirksam sein, wird davon die "
  "Wirksamkeit der übrigen Bestimmungen nicht berührt.")

S(0.3*cm)

# --- Signatures ---
H2("Unterschriften")
sig_table = Table(
    [[SignatureLine("sig_verant", "Für die Kundenorganisation (Verantwortlicher)"),
      SignatureLine("sig_auftrag", "Für den sharePAD-Betreiber (Auftragsverarbeiter)")]],
    colWidths=[8.5*cm, 8.5*cm],
)
sig_table.setStyle(TableStyle([
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("LEFTPADDING", (0,0), (-1,-1), 0),
    ("RIGHTPADDING", (0,0), (-1,-1), 0),
]))
story.append(sig_table)

story.append(PageBreak())

# ---------- Annex 1: Sub-processors ----------
H1("Anlage 1 – Sub-Auftragsverarbeiter")
P("Stand bei Vertragsschluss. Der sharePAD-Betreiber informiert die Kunden­"
  "organisation über Änderungen gemäß § 6 Abs. 2.")
S(0.2*cm)

subproc_header = ["Dienstleister", "Zweck", "Sitz / Region", "Verarbeitete Daten"]
subproc_rows = [
    ["Fly.io, Inc.", "Hosting der Anwendung, Runtime-Logs",
     "Rechenzentrum Frankfurt a. M.",
     "Sämtliche Anfragen (transient), Server-Logs"],
    ["Neon, Inc.", "Persistente PostgreSQL-Datenbank",
     "Frankfurt a. M. (AWS eu-central-1)",
     "Sämtliche in § 3 genannten Daten"],
    ["Functional Software, Inc. (Sentry)", "Fehler- und Performance-Monitoring",
     "EU-Region (de.sentry.io)",
     "Fehlermeldungen, Stacktraces, Umgebungsinformationen – ohne IP und Request-Header"],
    ["Mapbox, Inc.", "Geocoding, Entfernungsberechnung, Kartenkacheln",
     "USA (Drittland, SCC / DPF)",
     "Adressen und Geokoordinaten von Organisationen und Ressourcen"],
    ["Kaleido AI GmbH (remove.bg)", "Automatische Hintergrundentfernung bei Bild-Uploads",
     "Wien, Österreich",
     "Hochgeladene Bilddateien (Logos, Ressourcenbilder)"],
    ["Strato AG", "SMTP-Versand transaktionaler E-Mails",
     "Deutschland",
     "E-Mail-Adresse, Name, Einladungs- / Reset-Links"],
    ["Haufe-Lexware GmbH & Co. KG", "Rechnungsstellung für den sharePAD-Dienst",
     "Freiburg, Deutschland",
     "Kontaktdaten der Kundenorganisation und ihrer Administratoren"],
]
# wrap text cells with Paragraph
def wrap_row(row):
    return [Paragraph(c, small) for c in row]

data = [wrap_row(subproc_header)] + [wrap_row(r) for r in subproc_rows]
t = Table(data, colWidths=[4.2*cm, 4.0*cm, 3.5*cm, 5.3*cm], repeatRows=1)
t.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#efe7d8")),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#888888")),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("TOPPADDING", (0,0), (-1,-1), 3),
    ("BOTTOMPADDING", (0,0), (-1,-1), 3),
]))
story.append(t)
S(0.4*cm)
P("<b>Drittlandtransfer:</b> Die Übermittlung an Mapbox, Inc. (USA) erfolgt auf "
  "Grundlage des EU-US Data Privacy Framework (Art. 45 DSGVO) bzw. ergänzend "
  "auf Basis der Standardvertragsklauseln der EU-Kommission (Art. 46 Abs. 2 "
  "lit. c DSGVO). Alle übrigen Dienstleister verarbeiten Daten innerhalb der "
  "EU bzw. des EWR.")

story.append(PageBreak())

# ---------- Annex 2: TOMs ----------
H1("Anlage 2 – Technische und organisatorische Maßnahmen (TOMs)")
P("Der sharePAD-Betreiber setzt die folgenden Maßnahmen nach Art. 32 DSGVO um, "
  "um die Sicherheit der Verarbeitung zu gewährleisten. Die Maßnahmen werden "
  "regelmäßig überprüft und an den Stand der Technik angepasst.")

H3("1. Vertraulichkeit (Art. 32 Abs. 1 lit. b DSGVO)")
P("• Ausschließlich verschlüsselte Übertragung aller Anfragen per TLS (HTTPS).")
P("• Speicherung von Passwörtern ausschließlich als bcrypt-Hash; das Klartext-"
  "Passwort ist dem sharePAD-Betreiber nicht bekannt.")
P("• Speicherung von API-Schlüsseln angebundener Fremdanwendungen ausschließlich "
  "als SHA-256-Hash.")
P("• Rollen- und organisationsbezogene Zugriffskontrolle (Mandantentrennung): "
  "Mitglieder sehen nur Daten ihrer eigenen Organisation bzw. – bei Partner-"
  "Freigabe – nur die ausdrücklich freigegebenen Ressourcen.")
P("• Zeitlich begrenzte Sitzungen: 90 Tage für reguläre Mitglieder, 4 Stunden für "
  "administrative Sitzungen.")
P("• Getrennte administrative Konten zur Minimierung von Zugriffsrechten.")

H3("2. Integrität (Art. 32 Abs. 1 lit. b DSGVO)")
P("• Vollständige Änderungshistorie (Audit-Log) auf Reservierungen: Wer hat wann "
  "welche Änderung vorgenommen.")
P("• Eingabevalidierung und serverseitige Rechteprüfung bei allen schreibenden "
  "Operationen.")

H3("3. Verfügbarkeit und Belastbarkeit (Art. 32 Abs. 1 lit. b DSGVO)")
P("• Hosting der Anwendung und persistente Speicherung ausschließlich in "
  "Frankfurt a. M.")
P("• Tägliche automatisierte Datensicherungen der Datenbank.")
P("• Monitoring der Verfügbarkeit und Performance; Fehler- und Performance-"
  "Ereignisse werden an Sentry (EU-Region) übermittelt, ohne personenbezogene "
  "Zusatzinformationen (IP-Adresse und Request-Header sind in der Integration "
  "deaktiviert).")

H3("4. Verfahren zur regelmäßigen Überprüfung (Art. 32 Abs. 1 lit. d DSGVO)")
P("• Regelmäßige Aktualisierung der eingesetzten Software-Komponenten und "
  "Abhängigkeiten.")
P("• Überprüfung der Wirksamkeit der TOMs mindestens einmal jährlich sowie "
  "anlassbezogen.")

H3("5. Auftragskontrolle")
P("• Schriftliche Weisungen und Auftragsverarbeitungsverträge mit allen "
  "eingesetzten Sub-Auftragsverarbeitern gemäß Art. 28 DSGVO.")
P("• Dokumentation der Sub-Auftragsverarbeiter in Anlage 1; Information der "
  "Kundenorganisation bei Änderungen gemäß § 6 Abs. 2.")

H3("6. Datenminimierung und Speicherbegrenzung")
P("• Stammdaten eines Mitglieds werden ein Jahr nach Beendigung der Mitgliedschaft "
  "gelöscht.")
P("• Reservierungen werden ein Jahr nach der letzten Abrechnung anonymisiert.")
P("• Server-Logs werden beim Hoster nach 30 Tagen automatisch gelöscht.")
P("• Ereignisdaten in Sentry werden gemäß Standard-Aufbewahrung (derzeit ca. "
  "90 Tage) automatisch gelöscht.")


# ---------- build ----------
def header_footer(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFont("Helvetica", 8)
    canvas_obj.setFillColor(colors.HexColor("#888888"))
    canvas_obj.drawString(2*cm, 1.2*cm,
        "Auftragsverarbeitungsvertrag sharePAD – Robert Hölzl Cloud Platforms")
    canvas_obj.drawRightString(A4[0] - 2*cm, 1.2*cm,
        f"Seite {doc.page}")
    canvas_obj.restoreState()


frame = Frame(2*cm, 2*cm, A4[0] - 4*cm, A4[1] - 3.5*cm,
              leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
template = PageTemplate(id="main", frames=[frame], onPage=header_footer)
doc = BaseDocTemplate(OUT, pagesize=A4,
                      title="Auftragsverarbeitungsvertrag sharePAD",
                      author="Robert Hölzl Cloud Platforms",
                      subject="AVV gemäß Art. 28 DSGVO",
                      leftMargin=2*cm, rightMargin=2*cm,
                      topMargin=1.5*cm, bottomMargin=2*cm)
doc.addPageTemplates([template])
doc.build(story)
print("generated:", OUT)
