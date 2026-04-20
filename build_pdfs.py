# -*- coding: utf-8 -*-
"""Generate all sharePAD legal PDFs (AVV, AGB, Datenschutzerklaerung)."""
import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, PageBreak, Flowable, HRFlowable,
)

BASE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(BASE, "static")

# ---------- styles (shared) ----------
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


# ---------- flowables ----------
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
        sig_y = self.height - 2.6*cm
        c.setFillColor(colors.HexColor("#f5f0e8"))
        c.setStrokeColor(colors.HexColor("#888888"))
        c.rect(0, sig_y, self.width, 1.6*cm, stroke=1, fill=1)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(0, sig_y - 0.35*cm, "Unterschrift / Stempel")
        c.setFont("Helvetica-Bold", 9)
        c.drawString(0, sig_y - 0.75*cm, self.label)


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#bbbbbb"),
                      spaceBefore=4, spaceAfter=4)


# ---------- shared build helper ----------
def _header_footer_factory(footer_left):
    def header_footer(canvas_obj, doc):
        canvas_obj.saveState()
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(colors.HexColor("#888888"))
        canvas_obj.drawString(2*cm, 1.2*cm, footer_left)
        canvas_obj.drawRightString(A4[0] - 2*cm, 1.2*cm, f"Seite {doc.page}")
        canvas_obj.restoreState()
    return header_footer


def _render(out_path, story, title, author, subject, footer_left):
    frame = Frame(2*cm, 2*cm, A4[0] - 4*cm, A4[1] - 3.5*cm,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    template = PageTemplate(id="main", frames=[frame],
                            onPage=_header_footer_factory(footer_left))
    doc = BaseDocTemplate(out_path, pagesize=A4,
                          title=title, author=author, subject=subject,
                          leftMargin=2*cm, rightMargin=2*cm,
                          topMargin=1.5*cm, bottomMargin=2*cm)
    doc.addPageTemplates([template])
    doc.build(story)
    print("generated:", out_path)


# ========================================================================
# AVV
# ========================================================================
def build_avv(out_path):
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
    P("<b>Verantwortlicher</b> (nachfolgend \u201eKundenorganisation\u201c) – vom Kunden auszufüllen:")
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
    P("<b>Auftragsverarbeiter</b> (nachfolgend \u201esharePAD-Betreiber\u201c):")
    P("Robert Hölzl Cloud Platforms<br/>"
      "Traunsteinerstr. 44<br/>"
      "83093 Bad Endorf<br/>"
      "Deutschland<br/>"
      "E-Mail: robert.hoelzl@sharepad.de")
    S(0.25*cm)
    P("wird der folgende Vertrag über die Verarbeitung personenbezogener Daten im Auftrag "
      "(nachfolgend \u201eVertrag\u201c oder \u201eAVV\u201c) geschlossen. Er konkretisiert die Pflichten "
      "der Parteien zum Datenschutz, die sich aus den zwischen ihnen geltenden Allgemeinen "
      "Geschäftsbedingungen von sharePAD (nachfolgend \u201eAGB\u201c) ergeben.")

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
      "Leistungen nach den AGB. Eine Verarbeitung zu eigenen Zwecken des "
      "sharePAD-Betreibers findet – außerhalb der gesetzlich erlaubten Ausnahmen – "
      "nicht statt.")

    # --- § 2 ---
    H2("§ 2 Dauer des Auftrags")
    P("Die Laufzeit dieses Vertrags entspricht der Laufzeit der AGB. Er endet "
      "automatisch mit deren Beendigung, ohne dass es einer gesonderten Kündigung "
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
      "im Rahmen der AGB, dieses AVV und auf dokumentierte Weisung der "
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
      "Kommt keine Einigung zustande, sind beide Parteien berechtigt, die AGB "
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
      "Geokoordinaten an Mapbox, Inc. (USA) sowie die Ablage täglicher Datenbank-"
      "Backups in einem privaten GitHub-Repository bei GitHub, Inc. (USA). "
      "Grundlage ist jeweils der Angemessenheitsbeschluss zum EU-US Data Privacy "
      "Framework bzw. ergänzend Standardvertragsklauseln (Art. 46 Abs. 2 lit. c "
      "DSGVO). Weitere Einzelheiten sind in Anlage 1 aufgeführt.")

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
    P("Für die Haftung der Parteien gelten Art. 82 DSGVO sowie die Regelungen der "
      "AGB. Eine Haftungsbegrenzung in den AGB gilt auch für Ansprüche "
      "aus diesem AVV, soweit zwingendes Recht nicht entgegensteht.")

    # --- § 10 ---
    H2("§ 10 Löschung und Rückgabe nach Beendigung")
    P("(1) Nach Beendigung der AGB hat der sharePAD-Betreiber nach Wahl der "
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
    P("(1) Im Konfliktfall zwischen den Regelungen dieses AVV und der AGB "
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
        ["GitHub, Inc. (Microsoft-Tochter)",
         "Sicherungsablage tägliches DB-Backup (privates, zugriffsbeschränktes Repository, 30 Tage Aufbewahrung)",
         "USA (Drittland, SCC / DPF)",
         "Vollständiges Datenbank-Backup (alle in § 3 genannten Daten)"],
    ]
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
    P("<b>Drittlandtransfer:</b> Die Übermittlungen an Mapbox, Inc. (USA) und "
      "GitHub, Inc. (USA) erfolgen auf Grundlage des EU-US Data Privacy Framework "
      "(Art. 45 DSGVO) bzw. ergänzend auf Basis der Standardvertragsklauseln der "
      "EU-Kommission (Art. 46 Abs. 2 lit. c DSGVO). Alle übrigen Dienstleister "
      "verarbeiten Daten innerhalb der EU bzw. des EWR.")

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
    P("• Zusätzlich wird täglich eine vollständige Datenbanksicherung in ein privates, "
      "zugriffsbeschränktes GitHub-Repository übertragen. Diese Backups werden dort "
      "für maximal 30 Tage aufbewahrt und anschließend automatisch gelöscht. Zweck "
      "ist die kurzfristige Wiederherstellbarkeit bei Ausfall oder Datenverlust des "
      "Primär-Hosters.")
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
    P("• GitHub-Backups werden nach 30 Tagen automatisch gelöscht.")
    P("• Ereignisdaten in Sentry werden gemäß Standard-Aufbewahrung (derzeit ca. "
      "90 Tage) automatisch gelöscht.")

    _render(out_path, story,
            title="Auftragsverarbeitungsvertrag sharePAD",
            author="Robert Hölzl Cloud Platforms",
            subject="AVV gemäß Art. 28 DSGVO",
            footer_left="Auftragsverarbeitungsvertrag sharePAD – Robert Hölzl Cloud Platforms")


# ========================================================================
# AGB
# ========================================================================
def build_agb(out_path):
    story = []
    def P(t): story.append(Paragraph(t, body))
    def H1(t): story.append(Paragraph(t, h1))
    def H2(t): story.append(Paragraph(t, h2))
    def H3(t): story.append(Paragraph(t, h3))
    def S(h=0.2*cm): story.append(Spacer(1, h))

    H1("Allgemeine Geschäftsbedingungen (AGB)")
    story.append(Paragraph("für den Dienst <b>sharePAD</b>", body))
    P("Stand: 19.04.2026")
    S(0.4*cm)

    # § 1
    H2("§ 1 Geltungsbereich, Anbieter")
    P("(1) Diese Allgemeinen Geschäftsbedingungen (nachfolgend \u201eAGB\u201c) regeln die "
      "Nutzung des Internetdienstes sharePAD (abrufbar unter app.sharepad.de bzw. "
      "beta.sharepad.de) zwischen dem Anbieter und dem Kunden.")
    P("(2) Anbieter ist:")
    P("Robert Hölzl Cloud Platforms<br/>"
      "Traunsteinerstr. 44<br/>"
      "83093 Bad Endorf<br/>"
      "Deutschland<br/>"
      "E-Mail: robert.hoelzl@sharepad.de")
    P("(3) Die AGB gelten gegenüber Unternehmern (§ 14 BGB), insbesondere "
      "Organisationen wie Vereinen und Genossenschaften, sowie gegenüber "
      "Verbrauchern (§ 13 BGB). Besondere Regelungen für Verbraucher sind "
      "gesondert gekennzeichnet.")
    P("(4) Abweichende, entgegenstehende oder ergänzende Bedingungen des Kunden "
      "werden nur dann Vertragsbestandteil, wenn der Anbieter ihrer Geltung "
      "ausdrücklich in Textform zugestimmt hat.")

    # § 2
    H2("§ 2 Leistungsbeschreibung")
    P("(1) sharePAD ist eine webbasierte Plattform, mit der Organisationen "
      "gemeinschaftlich genutzte Ressourcen (z. B. Fahrzeuge, Lastenräder, Räume) "
      "unter ihren Mitgliedern verwalten, reservieren und abrechnen können.")
    P("(2) Der Anbieter stellt die Plattform im jeweils aktuellen Funktionsumfang "
      "als Software-as-a-Service bereit. Eine bestimmte Verfügbarkeit wird nicht "
      "zugesichert.")
    P("(3) <b>Support</b> erfolgt ausschließlich per E-Mail an "
      "robert.hoelzl@sharepad.de. Ein Anspruch auf Reaktion innerhalb einer "
      "bestimmten Frist besteht nicht.")

    # § 3
    H2("§ 3 Vertragsschluss")
    P("(1) Durch Registrierung eines Kontos bzw. einer Organisation in sharePAD "
      "gibt der Kunde ein Angebot auf Abschluss eines Nutzungsvertrags ab. Der "
      "Vertrag kommt mit der Bestätigung des Anbieters (in der Regel per E-Mail) "
      "oder mit der Freischaltung des Zugangs zustande.")
    P("(2) Der Kunde sichert zu, die bei der Registrierung angegebenen Daten "
      "wahrheitsgemäß und aktuell zu halten.")

    # § 4
    H2("§ 4 Tarife, 90-Tage-Demo")
    P("(1) sharePAD wird in folgenden Tarifen angeboten:")
    P("• <b>Free-Plan:</b> kostenfrei; Grundfunktionen zur Verwaltung und "
      "Reservierung stehen ohne zeitliche oder mengenmäßige Beschränkung zur "
      "Verfügung.")
    P("• <b>Pro-Plan:</b> 2,50 € netto je abrechnungsrelevanter Ressource (z. B. "
      "Fahrzeug) und Monat. Umsatzsteuer wird nach den jeweils geltenden "
      "steuerrechtlichen Vorschriften zusätzlich ausgewiesen, sofern einschlägig.")
    P("(2) <b>90-Tage-Demo:</b> Neue Kunden können den Pro-Funktionsumfang für "
      "90 Tage ab Registrierung kostenfrei nutzen. Nach Ablauf der Demo-Phase geht "
      "das Konto automatisch in den kostenpflichtigen Pro-Plan über, sofern der "
      "Kunde nicht zuvor auf den Free-Plan zurückwechselt oder den Vertrag "
      "gemäß § 6 kündigt. Der Anbieter weist rechtzeitig vor Ablauf der Demo-"
      "Phase per E-Mail auf den anstehenden Übergang hin.")

    # § 5
    H2("§ 5 Rechnung, Zahlung, SEPA-Mandat")
    P("(1) Der Anbieter stellt dem Kunden monatlich eine Rechnung auf Basis der "
      "Anzahl der vom Kunden genutzten Pro-Ressourcen. Maßgebend für die "
      "Abrechnung eines Kalendermonats ist die Anzahl der Pro-Ressourcen am "
      "<b>15. dieses Monats</b>.")
    P("(2) Die Rechnungsstellung erfolgt <b>am 1. des Folgemonats</b>. Der "
      "Rechnungsbetrag wird <b>wenige Tage danach</b> per SEPA-Lastschrift vom "
      "durch den Kunden hinterlegten Konto eingezogen. Eine gesonderte "
      "Zahlungsfrist besteht aufgrund des Lastschrifteinzugs nicht.")
    P("(3) Vor Beginn des kostenpflichtigen Nutzungszeitraums (insbesondere vor "
      "Übergang aus der 90-Tage-Demo in den Pro-Plan) hat der Kunde dem Anbieter "
      "ein <b>SEPA-Lastschriftmandat</b> zu erteilen. Der entsprechende "
      "Mandatsvordruck wird vom Anbieter bereitgestellt.")
    P("(4) Ankündigungsfrist (Pre-Notification) für SEPA-Lastschriften: 1 Bank­"
      "arbeitstag. Mit Erteilung des Mandats stimmt der Kunde dieser verkürzten "
      "Frist ausdrücklich zu.")
    P("(5) Kosten für vom Kunden zu vertretende Rücklastschriften (insbesondere "
      "mangels Kontodeckung oder aufgrund eines unberechtigten Widerrufs der "
      "Lastschrift) trägt der Kunde in tatsächlich entstandener Höhe.")

    # § 6
    H2("§ 6 Laufzeit und Kündigung")
    P("(1) Der Nutzungsvertrag wird auf unbestimmte Zeit geschlossen.")
    P("(2) Der Vertrag kann von beiden Parteien <b>monatlich zum Ende des "
      "laufenden Kalendermonats</b> ohne Angabe von Gründen gekündigt werden.")
    P("(3) Die Kündigung durch den Kunden erfolgt <b>ausschließlich per E-Mail</b> "
      "an robert.hoelzl@sharepad.de. Eine Kündigung über die Administrations­"
      "oberfläche oder auf anderem Weg ist nicht vorgesehen.")
    P("(4) Das Recht beider Parteien zur außerordentlichen Kündigung aus wichtigem "
      "Grund bleibt unberührt.")
    P("(5) Folgen der Beendigung hinsichtlich personenbezogener Daten richten sich "
      "nach dem AVV (insbesondere § 10 AVV).")

    # § 7
    H2("§ 7 Widerrufsrecht für Verbraucher")
    P("<i>Die nachfolgende Widerrufsbelehrung gilt nur, wenn der Kunde Verbraucher "
      "im Sinne des § 13 BGB ist. Unternehmern steht kein Widerrufsrecht zu.</i>")
    H3("Widerrufsbelehrung")
    P("<b>Widerrufsrecht</b>")
    P("Sie haben das Recht, binnen vierzehn Tagen ohne Angabe von Gründen diesen "
      "Vertrag zu widerrufen. Die Widerrufsfrist beträgt vierzehn Tage ab dem Tag "
      "des Vertragsabschlusses.")
    P("Um Ihr Widerrufsrecht auszuüben, müssen Sie uns (Robert Hölzl Cloud "
      "Platforms, Traunsteinerstr. 44, 83093 Bad Endorf, E-Mail: "
      "robert.hoelzl@sharepad.de) mittels einer eindeutigen Erklärung (z. B. ein "
      "mit der Post versandter Brief oder E-Mail) über Ihren Entschluss, diesen "
      "Vertrag zu widerrufen, informieren. Sie können dafür das beigefügte "
      "Muster-Widerrufsformular (Anhang A) verwenden; dies ist jedoch nicht "
      "vorgeschrieben.")
    P("Zur Wahrung der Widerrufsfrist reicht es aus, dass Sie die Mitteilung über "
      "die Ausübung des Widerrufsrechts vor Ablauf der Widerrufsfrist absenden.")
    P("<b>Folgen des Widerrufs</b>")
    P("Wenn Sie diesen Vertrag widerrufen, haben wir Ihnen alle Zahlungen, die "
      "wir von Ihnen erhalten haben, unverzüglich und spätestens binnen vierzehn "
      "Tagen ab dem Tag zurückzuzahlen, an dem die Mitteilung über Ihren Widerruf "
      "dieses Vertrags bei uns eingegangen ist. Für diese Rückzahlung verwenden "
      "wir dasselbe Zahlungsmittel, das Sie bei der ursprünglichen Transaktion "
      "eingesetzt haben, es sei denn, mit Ihnen wurde ausdrücklich etwas anderes "
      "vereinbart; in keinem Fall werden Ihnen wegen dieser Rückzahlung Entgelte "
      "berechnet.")
    P("Haben Sie verlangt, dass die Dienstleistungen während der Widerrufsfrist "
      "beginnen sollen, so haben Sie uns einen angemessenen Betrag zu zahlen, der "
      "dem Anteil der bis zu dem Zeitpunkt, zu dem Sie uns von der Ausübung des "
      "Widerrufsrechts hinsichtlich dieses Vertrags unterrichten, bereits "
      "erbrachten Dienstleistungen im Vergleich zum Gesamtumfang der im Vertrag "
      "vorgesehenen Dienstleistungen entspricht.")

    # § 8
    H2("§ 8 Pflichten des Kunden")
    P("(1) Der Kunde ist verpflichtet, die für die Nutzung des Dienstes "
      "erforderlichen Daten (Organisation, Kontakt, Zahlungsdaten) wahrheitsgemäß "
      "und aktuell anzugeben.")
    P("(2) Der Kunde hat seine Zugangsdaten vertraulich zu behandeln, sichere "
      "Passwörter zu wählen und Dritten keinen unbefugten Zugang zu seinem Konto "
      "zu gewähren.")
    P("(3) Der Kunde darf den Dienst nur zu rechtmäßigen Zwecken nutzen. "
      "Insbesondere dürfen keine Rechte Dritter, gesetzliche Vorschriften oder "
      "behördliche Auflagen verletzt werden.")
    P("(4) Ist der Kunde eine Organisation, die in sharePAD personenbezogene "
      "Daten Dritter (z. B. ihrer Mitglieder) verarbeitet, so ist er insoweit "
      "datenschutzrechtlich Verantwortlicher im Sinne des Art. 4 Nr. 7 DSGVO. "
      "Näheres regelt der AVV (§ 9).")

    # § 9
    H2("§ 9 Datenschutz, AVV")
    P("(1) Der Anbieter verarbeitet personenbezogene Daten gemäß seiner "
      "Datenschutzerklärung (abrufbar unter sharepad.de).")
    P("(2) Ist der Kunde eine Organisation, die in sharePAD personenbezogene Daten "
      "Dritter verarbeitet, schließen die Parteien zusätzlich den "
      "<b>Auftragsverarbeitungsvertrag (AVV)</b> nach Art. 28 DSGVO. Der AVV ist "
      "integraler Bestandteil dieser AGB.")

    # § 10
    H2("§ 10 Haftung")
    P("(1) Der Anbieter haftet uneingeschränkt für Vorsatz und grobe Fahrlässigkeit, "
      "für Schäden aus der Verletzung des Lebens, des Körpers oder der Gesundheit, "
      "bei arglistig verschwiegenen Mängeln sowie nach zwingenden gesetzlichen "
      "Vorschriften (insbesondere dem Produkthaftungsgesetz).")
    P("(2) Bei leicht fahrlässiger Verletzung wesentlicher Vertragspflichten "
      "(Kardinalpflichten, d. h. Pflichten, deren Erfüllung die ordnungsgemäße "
      "Durchführung des Vertrags überhaupt erst ermöglichen und auf deren "
      "Einhaltung der Kunde regelmäßig vertrauen darf) ist die Haftung auf den "
      "vertragstypischen, vorhersehbaren Schaden beschränkt, <b>höchstens jedoch "
      "auf die Summe der in den letzten zwölf (12) Monaten vor dem "
      "schadensbegründenden Ereignis vom Kunden tatsächlich an den Anbieter "
      "gezahlten Entgelte</b>.")
    P("(3) Im Übrigen ist die Haftung des Anbieters für leichte Fahrlässigkeit "
      "ausgeschlossen.")
    P("(4) Für Kunden im Free-Plan (ohne gezahlte Entgelte) gilt Absatz 2 mit der "
      "Maßgabe, dass die Haftung auf die in Absatz 1 genannten Tatbestände "
      "beschränkt ist.")
    P("(5) Zwingende verbraucherschützende Vorschriften bleiben unberührt.")

    # § 11
    H2("§ 11 Änderung der AGB")
    P("(1) Der Anbieter ist berechtigt, diese AGB mit einer Ankündigungsfrist von "
      "mindestens sechs (6) Wochen in Textform (insbesondere per E-Mail) zu ändern. "
      "Die geänderten AGB gelten als genehmigt, wenn der Kunde ihnen nicht innerhalb "
      "von sechs Wochen nach Zugang der Änderungsmitteilung in Textform widerspricht. "
      "Auf diese Folge wird der Anbieter in der Änderungsmitteilung ausdrücklich "
      "hinweisen.")
    P("(2) Widerspricht der Kunde fristgerecht, gilt die bisherige Fassung fort. "
      "Beide Parteien sind in diesem Fall berechtigt, den Vertrag zum nächsten "
      "ordentlichen Kündigungstermin (§ 6 Abs. 2) zu kündigen.")

    # § 12
    H2("§ 12 Schlussbestimmungen")
    P("(1) Es gilt deutsches Recht unter Ausschluss des UN-Kaufrechts. Gegenüber "
      "Verbrauchern gilt diese Rechtswahl nur insoweit, als dadurch nicht der "
      "Schutz entzogen wird, der durch zwingende Bestimmungen des Rechts des "
      "Staates gewährt wird, in dem der Verbraucher seinen gewöhnlichen "
      "Aufenthalt hat.")
    P("(2) Ausschließlicher Gerichtsstand für alle Streitigkeiten aus oder im "
      "Zusammenhang mit diesem Vertrag ist Rosenheim, soweit der Kunde Kaufmann, "
      "juristische Person des öffentlichen Rechts oder öffentlich-rechtliches "
      "Sondervermögen ist.")
    P("(3) Sollten einzelne Bestimmungen dieser AGB unwirksam oder undurchführbar "
      "sein oder werden, bleibt die Wirksamkeit der übrigen Bestimmungen unberührt.")
    P("(4) Hinweis nach § 36 VSBG: Der Anbieter ist nicht bereit und nicht "
      "verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucher­"
      "schlichtungsstelle teilzunehmen. Die Europäische Kommission stellt eine "
      "Plattform zur Online-Streitbeilegung (OS) unter "
      "https://ec.europa.eu/consumers/odr/ bereit.")

    story.append(PageBreak())

    # Anhang A
    H1("Anhang A – Muster-Widerrufsformular")
    P("(Wenn Sie den Vertrag widerrufen wollen, füllen Sie bitte dieses Formular "
      "aus und senden Sie es zurück.)")
    S(0.2*cm)
    P("An Robert Hölzl Cloud Platforms, Traunsteinerstr. 44, 83093 Bad Endorf, "
      "E-Mail: robert.hoelzl@sharepad.de:")
    S(0.15*cm)
    P("Hiermit widerrufe(n) ich/wir (*) den von mir/uns (*) abgeschlossenen "
      "Vertrag über die Erbringung der folgenden Dienstleistung (*):")
    S(0.5*cm)
    P("____________________________________________________________")
    S(0.3*cm)
    P("Bestellt am (*) / erhalten am (*): ____________________________")
    S(0.3*cm)
    P("Name des/der Verbraucher(s): ________________________________")
    S(0.3*cm)
    P("Anschrift des/der Verbraucher(s): ____________________________")
    S(0.3*cm)
    P("____________________________________________________________")
    S(0.3*cm)
    P("Unterschrift des/der Verbraucher(s) (nur bei Mitteilung auf Papier): "
      "____________________________")
    S(0.3*cm)
    P("Datum: ____________________________")
    S(0.3*cm)
    P("(*) Unzutreffendes streichen.")

    _render(out_path, story,
            title="AGB sharePAD",
            author="Robert Hölzl Cloud Platforms",
            subject="Allgemeine Geschäftsbedingungen sharePAD",
            footer_left="AGB sharePAD – Robert Hölzl Cloud Platforms")


# ========================================================================
# Datenschutzerklärung
# ========================================================================
def build_datenschutz(out_path):
    story = []
    def P(t): story.append(Paragraph(t, body))
    def H1(t): story.append(Paragraph(t, h1))
    def H2(t): story.append(Paragraph(t, h2))
    def H3(t): story.append(Paragraph(t, h3))
    def S(h=0.2*cm): story.append(Spacer(1, h))

    H1("Datenschutzerklärung für sharePAD")
    P("Stand: 19.04.2026")
    S(0.3*cm)

    # 1
    H2("1. Einleitung und Geltungsbereich")
    P("Diese Datenschutzerklärung informiert über die Verarbeitung personenbezogener "
      "Daten im Zusammenhang mit dem Internetdienst sharePAD, der unter den Adressen "
      "app.sharepad.de und beta.sharepad.de erreichbar ist. sharePAD ermöglicht es "
      "Organisationen (z. B. Carsharing-Vereinen), gemeinschaftlich genutzte "
      "Ressourcen wie Fahrzeuge unter ihren Mitgliedern zu verwalten und zu "
      "reservieren.")
    P("Ziel dieser Erklärung ist es, die Verarbeitungen nachvollziehbar zu machen "
      "und über die Rechte nach der Europäischen Datenschutz-Grundverordnung "
      "(DSGVO) sowie dem Bundesdatenschutzgesetz (BDSG) zu informieren.")

    # 2
    H2("2. Verantwortlicher und Rollenverteilung")
    P("sharePAD wird von Organisationen (nachfolgend \u201eKundenorganisation\u201c) "
      "eingesetzt, um die Ressourcennutzung ihrer Mitglieder zu organisieren. "
      "Datenschutzrechtlich ergibt sich daraus folgende Aufteilung:")
    P("• Für die personenbezogenen Daten der Mitglieder (Nutzer der "
      "Kundenorganisation) ist die jeweilige Kundenorganisation Verantwortlicher "
      "im Sinne des Art. 4 Nr. 7 DSGVO. Sie holt von ihren Mitgliedern die "
      "erforderliche Einwilligung bzw. die vertragliche Grundlage ein und "
      "entscheidet über Zwecke und Mittel der Verarbeitung.")
    P("• Der Betreiber von sharePAD verarbeitet diese Mitgliederdaten "
      "ausschließlich im Auftrag der Kundenorganisation als Auftragsverarbeiter "
      "gemäß Art. 28 DSGVO auf Basis eines Auftragsverarbeitungsvertrags (AVV).")
    P("• Für die direkte Vertragsbeziehung zwischen dem sharePAD-Betreiber und den "
      "Administratoren der Kundenorganisation (Registrierung, Abrechnung des "
      "Dienstes, Support-Kommunikation) ist der sharePAD-Betreiber selbst "
      "Verantwortlicher.")
    P("Betreiber und in diesem Umfang Verantwortlicher ist:")
    P("Robert Hölzl Cloud Platforms<br/>"
      "Traunsteinerstr. 44<br/>"
      "83093 Bad Endorf<br/>"
      "Deutschland")

    # 3
    H2("3. Kontakt für Datenschutzanfragen")
    P("Für Fragen zur Verarbeitung personenbezogener Daten und zur Ausübung der "
      "unten genannten Betroffenenrechte steht folgende Kontaktadresse zur "
      "Verfügung:")
    P("E-Mail: robert.hoelzl@sharepad.de")
    P("Ein Datenschutzbeauftragter ist nicht bestellt, da die gesetzlichen "
      "Schwellenwerte nach § 38 BDSG nicht erreicht werden. Betroffene, deren "
      "Daten im Auftrag einer Kundenorganisation verarbeitet werden, wenden sich "
      "für Auskunfts-, Berichtigungs- und Löschbegehren zusätzlich direkt an ihre "
      "Kundenorganisation.")

    # 4
    H2("4. Kategorien verarbeiteter personenbezogener Daten")
    P("sharePAD verarbeitet folgende Kategorien personenbezogener Daten:")
    H3("4.1 Stammdaten der Mitglieder")
    P("• Vor- und Nachname")
    P("• E-Mail-Adresse")
    P("• Telefonnummer")
    P("• Postanschrift (Straße, Postleitzahl, Ort)")
    P("• Mitgliedsnummer innerhalb der Kundenorganisation")
    P("• Rolle innerhalb der Kundenorganisation (Mitglied, Supervisor, Administrator)")
    P("• Datum der Beendigung der Mitgliedschaft (sofern eine Kündigung "
      "eingetragen wurde)")
    H3("4.2 Authentifizierungsdaten")
    P("• Passwort, ausschließlich gespeichert als bcrypt-Hash (das Klartext-"
      "Passwort ist dem Betreiber nicht bekannt)")
    P("• Sitzungs-Token (JSON Web Token), das nach erfolgreicher Anmeldung im "
      "Browser des Mitglieds im localStorage abgelegt wird. Für Mitglieder ist das "
      "Token 90 Tage gültig, für administrative Sitzungen nur 4 Stunden.")
    P("• Bei angebundenen Fremdanwendungen zusätzlich: API-Schlüssel, gespeichert "
      "als SHA-256-Hash.")
    H3("4.3 Reservierungsdaten")
    P("• Reservierungen von Ressourcen mit Start- und Endzeitpunkt, optionalem "
      "Kommentar und Bezug zum reservierenden Mitglied.")
    P("• Vollständige Änderungshistorie jeder Reservierung (Audit-Log): Wer hat "
      "wann welche Änderung vorgenommen. Die Historie bleibt auch bei "
      "Stornierung erhalten.")
    P("• Hilfsdaten zur Entfernungsberechnung (zwischengespeicherte Koordinaten "
      "zu Ressourcen-Standorten relativ zum Mitglied).")
    H3("4.4 Daten der Kundenorganisation")
    P("• Name, Kurzname und Adresse der Organisation")
    P("• Geografische Koordinaten (aus der Adresse ermittelt)")
    P("• Optional ein Organisations-Logo")
    P("• Vertrags- und Abrechnungsstatus")
    H3("4.5 Technische Daten")
    P("• Server-Logs des Hosters (u. a. IP-Adresse, Zeitstempel, aufgerufener "
      "Pfad, HTTP-Statuscode). Diese enthalten keine fachlichen Inhalte der "
      "Anfragen.")
    P("• Fehler- und Performance-Ereignisse, die im Fehlerfall an den Monitoring-"
      "Dienst Sentry übermittelt werden. Personenbezogene Zusatzinformationen "
      "(PII) sind in der Sentry-Integration ausdrücklich deaktiviert; IP-Adressen "
      "und Request-Header werden nicht an Sentry übermittelt.")

    # 5
    H2("5. Zwecke und Rechtsgrundlagen der Verarbeitung")
    H3("5.1 Betrieb der Reservierungsplattform")
    P("Die Stammdaten und Reservierungsdaten werden verarbeitet, um den Betrieb "
      "der Plattform (Anlegen, Bearbeiten und Löschen von Reservierungen, "
      "Kontaktaufnahme unter Mitgliedern, Abrechnung durch die Administration der "
      "Kundenorganisation) zu ermöglichen. Rechtsgrundlage ist Art. 6 Abs. 1 "
      "lit. b DSGVO (Vertrag zwischen Mitglied und Kundenorganisation) in "
      "Verbindung mit Art. 28 DSGVO (Verarbeitung im Auftrag) sowie ergänzend "
      "Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an einer funktionsfähigen "
      "gemeinsamen Nutzung der Ressourcen).")
    H3("5.2 Anzeige von Kontaktdaten zwischen Mitgliedern")
    P("Um es Mitgliedern zu ermöglichen, den aktuellen Nutzer einer Ressource zu "
      "kontaktieren (z. B. bei Abholung oder Verspätung), werden in den "
      "Reservierungen Name, E-Mail-Adresse und Telefonnummer des reservierenden "
      "Mitglieds innerhalb der Organisation angezeigt. Rechtsgrundlage: Art. 6 "
      "Abs. 1 lit. b DSGVO sowie Art. 6 Abs. 1 lit. f DSGVO.")
    H3("5.3 Authentifizierung")
    P("E-Mail-Adresse und Passwort-Hash werden ausschließlich zur Anmeldung und "
      "zur Absicherung des Zugangs verarbeitet. Rechtsgrundlage: Art. 6 Abs. 1 "
      "lit. b DSGVO.")
    H3("5.4 Versand transaktionaler E-Mails")
    P("Bei Anlage eines Mitglieds, bei Anforderung eines Passwort-Resets und bei "
      "Bestätigung einer neu registrierten Organisation versendet sharePAD "
      "Einladungs- bzw. Bestätigungsmails über einen deutschen SMTP-Dienstleister. "
      "Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO.")
    H3("5.5 Abrechnung")
    P("Für die Rechnungsstellung des sharePAD-Dienstes gegenüber der "
      "Kundenorganisation werden Abrechnungsdaten an einen externen "
      "Buchhaltungsdienstleister (Haufe-Lexware) übermittelt. Rechtsgrundlage: "
      "Art. 6 Abs. 1 lit. b und lit. c DSGVO.")
    H3("5.6 Adress-Geocoding und Entfernungsberechnung")
    P("Adressen von Organisationen und Mitgliedern werden einmalig in geografische "
      "Koordinaten umgewandelt, um die Entfernung zwischen Mitgliedern und "
      "Ressourcen in der Oberfläche darstellen zu können. Hierfür wird der Dienst "
      "Mapbox eingesetzt. Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO (berechtigtes "
      "Interesse an einer nutzbaren Kartendarstellung).")
    H3("5.7 Bildverarbeitung")
    P("Beim Hochladen von Organisations- oder Ressourcen-Logos wird optional der "
      "Bildhintergrund automatisiert entfernt. Hierfür wird die Bilddatei an den "
      "Dienst remove.bg übermittelt. Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO.")
    H3("5.8 Fehler- und Performance-Tracking")
    P("Zur Sicherung der Stabilität und Sicherheit des Dienstes werden "
      "Fehlerereignisse und Performance-Daten an den Dienst Sentry (EU-Region) "
      "übermittelt. Die Übermittlung personenbezogener Zusatzinformationen "
      "(IP-Adresse, Request-Header) ist in der Konfiguration deaktiviert. "
      "Rechtsgrundlage: Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an "
      "einem fehlerfreien Dienst).")
    H3("5.9 Datensicherung (Backups)")
    P("Zur Gewährleistung der Wiederherstellbarkeit wird die Datenbank täglich "
      "automatisch gesichert. Zusätzlich wird eine vollständige Datenbank­"
      "sicherung täglich in ein privates, zugriffsbeschränktes GitHub-Repository "
      "bei GitHub, Inc. übertragen; diese Backups werden dort für maximal 30 Tage "
      "aufbewahrt und anschließend automatisch gelöscht. Rechtsgrundlage: Art. 6 "
      "Abs. 1 lit. f DSGVO (berechtigtes Interesse an einer robusten "
      "Wiederherstellbarkeit bei Ausfall oder Datenverlust des Primär-Hosters) "
      "sowie Art. 32 DSGVO.")

    # 6
    H2("6. Speicherdauer und Löschung")
    P("• Stammdaten eines Mitglieds werden ein Jahr nach der Kündigung gelöscht.")
    P("• Reservierungen werden ein Jahr nach der letzten Abrechnung anonymisiert. "
      "Danach bleibt die Reservierung ohne Bezug zum Mitglied zu statistischen "
      "Zwecken erhalten.")
    P("• Das Audit-Log einer Reservierung teilt deren Lebensdauer und wird "
      "zusammen mit der Anonymisierung von Personenbezügen befreit.")
    P("• Server-Logs des Hosters (fly.io) werden nach 30 Tagen automatisch durch "
      "den Hoster gelöscht.")
    P("• GitHub-Backups (§ 5.9) werden nach 30 Tagen automatisch gelöscht.")
    P("• Fehler- und Performance-Ereignisse in Sentry werden gemäß der "
      "Standard-Aufbewahrung des Dienstes (derzeit ca. 90 Tage) automatisch "
      "gelöscht.")
    P("• Abrechnungsdaten zwischen sharePAD und den nutzenden Organisationen "
      "werden entsprechend der handels- und steuerrechtlichen Aufbewahrungsfristen "
      "(bis zu 10 Jahre, § 147 AO) gespeichert.")

    # 7
    H2("7. Empfänger und Sub-Auftragsverarbeiter")
    P("sharePAD setzt zur Erbringung des Dienstes folgende Auftragsverarbeiter "
      "bzw. Dienstleister ein. Mit allen eingesetzten Dienstleistern bestehen die "
      "datenschutzrechtlich erforderlichen Verträge nach Art. 28 DSGVO.")
    S(0.15*cm)

    header = ["Dienstleister", "Zweck", "Sitz / Region", "Verarbeitete Daten"]
    rows = [
        ["Fly.io (Fly.io, Inc.)", "Hosting der Anwendung, Runtime-Logs",
         "Rechenzentrum Frankfurt a. M.",
         "Sämtliche Anfragen (transient), Server-Logs"],
        ["Neon (Neon, Inc.)", "Persistente PostgreSQL-Datenbank",
         "Frankfurt a. M. (AWS eu-central-1)",
         "Sämtliche in Abschnitt 4 genannten Daten"],
        ["Sentry (Functional Software, Inc., EU-Region)",
         "Fehler- und Performance-Monitoring",
         "Deutschland (de.sentry.io)",
         "Fehlermeldungen, Stacktraces, Umgebungsinformationen – ohne IP-Adresse und ohne Request-Header"],
        ["Mapbox (Mapbox, Inc.)",
         "Geocoding, Entfernungsberechnung, Kartenkacheln",
         "USA (Drittland – siehe Abschnitt 8)",
         "Adressen von Organisationen, Mitgliedern und geografische Koordinaten von Ressourcen"],
        ["remove.bg (Kaleido AI GmbH)",
         "Automatische Hintergrundentfernung bei Bild-Uploads",
         "Wien, Österreich",
         "Hochgeladene Bilddateien (Logos, Ressourcenbilder)"],
        ["Strato (Strato AG)", "SMTP-Versand transaktionaler E-Mails",
         "Deutschland",
         "E-Mail-Adresse, Name, Einladungs-/Reset-Links"],
        ["Haufe-Lexware GmbH & Co. KG", "Rechnungsstellung für den sharePAD-Dienst",
         "Freiburg, Deutschland",
         "Kontaktdaten der Kundenorganisation und ihrer Administratoren"],
        ["GitHub, Inc. (Microsoft-Tochter)",
         "Sicherungsablage tägliches DB-Backup (privates Repository, 30 Tage Aufbewahrung)",
         "USA (Drittland – siehe Abschnitt 8)",
         "Vollständiges Datenbank-Backup (alle in Abschnitt 4 genannten Daten)"],
    ]
    def wrap_row(row):
        return [Paragraph(c, small) for c in row]
    data = [wrap_row(header)] + [wrap_row(r) for r in rows]
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

    # 8
    H2("8. Datenübermittlung in Drittländer")
    P("Der Dienst Mapbox wird durch die Mapbox, Inc. mit Sitz in den USA "
      "betrieben. Eine Übermittlung von Adressen (ohne Nutzerdaten!) und "
      "Koordinaten von Ressourcen in die USA findet einmal bei neuen Adressen "
      "statt. Ebenso werden tägliche Datenbank-Backups an ein privates Repository "
      "bei GitHub, Inc. (USA) übertragen. Die Übermittlung erfolgt jeweils auf "
      "Grundlage der Standardvertragsklauseln der EU-Kommission (Art. 46 Abs. 2 "
      "lit. c DSGVO) bzw. – soweit der jeweilige Dienstleister unter dem EU-US "
      "Data Privacy Framework zertifiziert ist – auf Grundlage eines "
      "Angemessenheitsbeschlusses der EU-Kommission nach Art. 45 DSGVO. Alle "
      "übrigen Dienstleister verarbeiten die Daten ausschließlich innerhalb der "
      "EU bzw. des EWR.")

    # 9
    H2("9. Weitergabe an Partner-Organisationen")
    P("Eine Kundenorganisation kann einzelne Ressourcen für sogenannte "
      "Partner-Organisationen freigeben (sog. Quernutzung). Mitglieder einer "
      "Partner-Organisation können diese Ressourcen reservieren. In diesem Fall "
      "erhalten die Administratoren der jeweils anderen Organisation Einblick in "
      "die Reservierungen der freigegebenen Ressource, einschließlich Name, "
      "E-Mail-Adresse, Telefonnummer und Adresse des reservierenden Mitglieds. "
      "Die interne Mitgliedsnummer wird dabei nicht geteilt. Rechtsgrundlage ist "
      "Art. 6 Abs. 1 lit. b DSGVO in Verbindung mit der zwischen den "
      "Organisationen getroffenen Kooperationsvereinbarung.")

    # 10
    H2("10. Datenübernahme aus dem Vorgängersystem (elkato)")
    P("Kundenorganisationen, die zuvor das System elkato eingesetzt haben, können "
      "ihre Bestandsdaten einmalig oder wiederholt während einer Evaluierungsphase "
      "in sharePAD übernehmen. Dabei werden Stammdaten der Mitglieder (Name, "
      "Adresse, Kontaktdaten, Mitgliedsnummer, Austrittsdatum), Ressourcen und "
      "vorhandene Reservierungen importiert. Bestehende Passwörter liegen im "
      "elkato-System als MD5-Hash vor; sie werden beim erstmaligen Login eines "
      "Mitglieds in sharePAD in einen bcrypt-Hash überführt und anschließend in "
      "der ursprünglichen Form verworfen.")

    # 11
    H2("11. Cookies, localStorage und Tracking")
    P("sharePAD setzt keine Tracking-Cookies und bindet keine Analytics- oder "
      "Werbe-Drittanbieter ein. Nach erfolgreicher Anmeldung wird ausschließlich "
      "ein Sitzungs-Token (JSON Web Token) im localStorage des Browsers abgelegt, "
      "um das Mitglied bei folgenden Anfragen wiederzuerkennen. Dieses Token ist "
      "technisch erforderlich; eine Einwilligung nach § 25 TTDSG ist hierfür "
      "nicht notwendig.")

    # 12
    H2("12. Technische und organisatorische Maßnahmen")
    P("• Verschlüsselte Übertragung aller Anfragen per TLS (HTTPS)")
    P("• Speicherung von Passwörtern ausschließlich als bcrypt-Hash; API-Schlüssel "
      "als SHA-256-Hash")
    P("• Zeitlich begrenzte Sitzungen (90 Tage für reguläre Mitglieder, 4 Stunden "
      "für administrative Sitzungen)")
    P("• Rollen- und organisationsbezogene Zugriffskontrolle auf alle Daten "
      "(Mandantentrennung)")
    P("• Hosting und persistente Speicherung ausschließlich in Frankfurt a. M.")
    P("• Tägliche automatisierte Datensicherungen der Datenbank")
    P("• Zusätzliche tägliche Datenbanksicherung in ein privates, zugriffs­"
      "beschränktes GitHub-Repository mit 30 Tagen Aufbewahrung (s. Abschnitt 5.9)")

    # 13
    H2("13. Rechte der betroffenen Personen")
    P("Betroffene Personen können gegenüber dem Verantwortlichen jederzeit folgende "
      "Rechte geltend machen:")
    P("• Recht auf Auskunft (Art. 15 DSGVO)")
    P("• Recht auf Berichtigung (Art. 16 DSGVO)")
    P("• Recht auf Löschung (Art. 17 DSGVO)")
    P("• Recht auf Einschränkung der Verarbeitung (Art. 18 DSGVO)")
    P("• Recht auf Datenübertragbarkeit (Art. 20 DSGVO)")
    P("• Recht auf Widerspruch gegen die Verarbeitung auf Grundlage berechtigter "
      "Interessen (Art. 21 DSGVO)")
    P("• Recht auf Widerruf einer erteilten Einwilligung mit Wirkung für die "
      "Zukunft (Art. 7 Abs. 3 DSGVO)")
    P("Daneben besteht das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu "
      "beschweren (Art. 77 DSGVO). Für den sharePAD-Betreiber ist das zuständig:")
    P("Bayerisches Landesamt für Datenschutzaufsicht (BayLDA)<br/>"
      "Promenade 18, 91522 Ansbach<br/>"
      "https://www.lda.bayern.de/")

    # 14
    H2("14. Stand und Aktualisierung dieser Erklärung")
    P("Diese Datenschutzerklärung wird bei Änderungen der technischen Grundlagen "
      "oder der eingesetzten Dienstleister aktualisiert. Der Stand am Anfang "
      "dieses Dokuments gibt den Zeitpunkt der letzten Aktualisierung an.")

    _render(out_path, story,
            title="Datenschutzerklärung sharePAD",
            author="Robert Hölzl Cloud Platforms",
            subject="Datenschutzerklärung sharePAD",
            footer_left="Datenschutzerklärung sharePAD – Robert Hölzl Cloud Platforms")


# ========================================================================
# main
# ========================================================================
TARGETS = {
    "avv": (build_avv, os.path.join(STATIC, "Auftragsverarbeitungsvertrag.pdf")),
    "agb": (build_agb, os.path.join(STATIC, "AGB.pdf")),
    "datenschutz": (build_datenschutz, os.path.join(STATIC, "Datenschutzerklärung.pdf")),
}


def main(argv):
    if not os.path.isdir(STATIC):
        os.makedirs(STATIC, exist_ok=True)
    selection = argv[1:] if len(argv) > 1 else list(TARGETS.keys())
    for key in selection:
        if key not in TARGETS:
            print(f"unknown target: {key} (known: {', '.join(TARGETS)})", file=sys.stderr)
            sys.exit(2)
        fn, out = TARGETS[key]
        fn(out)


if __name__ == "__main__":
    main(sys.argv)
