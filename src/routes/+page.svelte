<!-- Hero Section -->
<div class="relative min-h-screen overflow-hidden bg-gradient-to-br from-warm-50 via-white to-primary-50">
	<!-- Decorative gradient orbs -->
	<div class="absolute top-20 left-10 w-72 h-72 bg-primary-200/40 rounded-full blur-3xl"></div>
	<div class="absolute bottom-40 right-10 w-96 h-96 bg-accent-200/30 rounded-full blur-3xl"></div>
	<div class="absolute top-1/2 left-1/3 w-64 h-64 bg-primary-100/50 rounded-full blur-2xl"></div>

	<!-- Hero content -->
	<div class="relative z-10 mx-auto max-w-7xl px-6 pt-16 pb-24 lg:px-8">
		<div class="flex flex-col lg:flex-row items-center gap-12 lg:gap-16">
			<!-- Text content -->
			<div class="flex-1 text-center lg:text-left">
				<div class="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6">
					<span class="text-gradient">share</span><span class="text-gradient-blue">PAD</span>
				</div>
				<p class="text-xl sm:text-2xl text-warm-600 font-medium mb-8 max-w-xl mx-auto lg:mx-0">
					Teilen leicht gemacht - für Autos, Lastenräder und alles, was Ihre Community verbindet
				</p>
				<div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
					<a
						href="https://app.sharepad.de"
						class="inline-block px-8 py-4 rounded-xl font-semibold bg-gradient-to-r from-primary-500 to-primary-600 text-white hover:from-primary-600 hover:to-primary-700 shadow-lg hover:shadow-xl transition-all duration-300 hover:-translate-y-0.5"
					>
						Jetzt starten
					</a>
					<a
						href="#intro"
						class="inline-block px-8 py-4 rounded-xl font-semibold bg-white/80 text-warm-700 hover:bg-white border border-warm-200 shadow-md hover:shadow-lg transition-all duration-300"
					>
						Mehr erfahren
					</a>
				</div>
			</div>

			<!-- Phone mockup with floating animation -->
			<div class="flex-1 flex justify-center lg:justify-end">
				<img
					src="mobile-with-app.png"
					alt="Phone with sharePAD App"
					class="h-[50vh] sm:h-[55vh] lg:h-[65vh] max-h-[600px] object-contain drop-shadow-2xl animate-float"
				/>
			</div>
		</div>
	</div>

	<!-- Scroll indicator -->
	{#if topOfPage}
		<div class="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 animate-pulse-soft" transition:fade>
			<span class="text-warm-500 text-sm font-medium">Scroll</span>
			<ChevronDoubleDownIcon class="w-8 h-8 text-primary-400" />
		</div>
	{/if}
</div>

<!-- Transition-Image to first Section -->
<div class="relative">
	<img src="hero-background.png" alt="Menschen um Auto und Lastenrad" class="w-full" />
	<div class="absolute top-0 right-0 left-0 h-1/2 bg-gradient-to-b from-primary-50/80 to-transparent"></div>
</div>

<Section side="left" title="So funktioniert sharePAD" id="intro">
	<P>
		<CalendarClockIcon class="float-right ml-4 text-[5em] text-accent-500" />
		sharePAD ist eine Sharing&shy;platform, um in Organisationen oder kleinen Gruppen Ressourcen wie
		Autos, Räder, Räume, usw. gemeinsam zu nutzen. Kern von sharePAD ist ein intuitiv zu benutzendes
		Reservierungssystem. Damit kann jeder Nutzer sehen welche Ressource(n) in welchen Zeiträumen verfügbar
		sind, und diese ggf. reservieren. Rund um dieses Reservierungssystem sind weitere Dienste verfügbar
		bzw. geplant, um den organisatorischen Aufwand so gering wie möglich zu halten:
	</P>

	<UL>
		<LI>
			<Badge title="Geplant" />
			Abrechnung am Monats/Quartalsende<br />
			<span class="italic text-warm-500">
				(Aktuell existiert hierfür eine Schnittstelle zum Abrechnungssystem vom Vaterstettner
				Vorgängersystem
				<A href="https://sourceforge.net/projects/elkatoabrechnung/">elkato</A>)
			</span>
		</LI>
		<LI>
			<Badge title="Geplant" />
			<span class="font-bold">Für KFZ:</span>
			Optional elektronisches Fahrtenbuch zur Kilometererfassung
		</LI>
		<LI>
			<Badge title="Geplant" />
			<span class="font-bold">Für KFZ:</span> Optional Smartcard-basiertes Zutrittskontrollsystem um
			sicherzustellen, dass ein Auto nur von Nutzern mit einer entsprechenden Reservierung aufgesperrt
			werden kann.
		</LI>
		<LI>
			<Badge title="Geplant" />
			<span class="font-bold">Für e-Autos:</span> Berücksichtigung des erwarteten Batterieladezustands
			bei Reservierungen.
		</LI>
		<LI>
			Partnerschaften mit Nachbarorganisationen, so dass deren Mitglieder die eigenen Ressourcen
			mitnutzen können.
		</LI>
	</UL>
</Section>

<Section side="right" title="Perfekt für Ihre Community" id="audience" variant="highlighted">
	<P>
		<AccountQuestionIcon class="float-right ml-4 text-[5em] text-accent-500" />
		sharePAD richtet sich an Communities wie Vereine, Genossenschaften, aber auch Nachbarschaften oder
		kleine Firmen. I.d.R. handelt es sich dabei um ehrenamtlich geführte Organisationen oder Gruppen
		aus Privatpersonen die nur ein sehr geringes Budget haben und für die andere Lösungen viel zu teuer
		sind.
	</P>

	<P>
		Da diese Zielgruppe oft keine IT-Kenntnisse hat, besitzt sharePAD des Weiteren eine bewusst
		einfach gehaltene Administrationsoberfläche. Diese erlaubt es jedem, schnell und unkompliziert
		eine Organisation einzurichten und zu verwalten.
	</P>

	<P>
		sharePAD wird in Kooperation mit den
		<A href="https://www.carsharing-vaterstetten.de/">Vaterstettner Autoteilern e.V.</A>
		entwickelt, um deren bestehendes Carsharing-Reservierungssystem <A href="https://www.elkato.de/"
			>"elkato"</A
		>
		durch ein modernes, intuitives System zu ersetzen. Da elkato Ende 2027 außer Betrieb genommen wird,
		bietet sharePAD für alle Organisationen die elkato aktuell nutzen, zusätzlich eine Migration mit
		wenigen Klicks sowie einen Testbetrieb.
	</P>
</Section>

<Section side="left" title="Preise" id="pricing">
	<P>
		<CashMultipleIcon class="float-left mr-4 text-[4em] text-accent-500" />
		Für <em>jede Ressource</em> muss jeweils einer der folgenden Tarife gewählt werden. D.h.
		innerhalb einer Organisation können die beiden Tarife beliebig kombiniert werden. Man zahlt also
		nur, was man braucht. Eine Ressource kann zu einem späteren Zeitpunkt auch jederzeit von
		<em>Free</em> zu <em>Pro</em> geupgradet werden.
	</P>

	<div class="flex w-full flex-row flex-wrap gap-6 mt-8">
		<Plan title="Free" light class="flex-1 min-w-[280px] xl:max-w-[45%]" cta="Kostenlos starten" ctaHref="https://app.sharepad.de/register">
			<UL class="m-5 text-left">
				<LI>beliebig viele Ressourcen</LI>
				<LI>beliebig viele Nutzer</LI>
				<LI>beliebig viele Reservierungen</LI>
				<LI>beliebig viele Partner&shy;organisationen</LI>
				<LI><b>kostenlos</b></LI>
			</UL>
		</Plan>

		<Plan title="Pro" recommended class="flex-1 min-w-[280px] xl:max-w-[45%]" cta="Pro wählen" ctaHref="https://app.sharepad.de/register">
			<div class="m-5 mb-0 text-warm-600">Alles wie in <b>Free</b> plus:</div>
			<UL class="m-5 text-left">
				<LI>Datenexport für Abrechnung</LI>
				<LI>Anbindung an Zutritts&shy;kontroll&shy;system <br /><em class="text-warm-500">(sobald verfügbar)</em></LI>
				<LI>Anbindung an elektronisches Fahrtenbuch <br /><em class="text-warm-500">(sobald verfügbar)</em></LI>
				<LI>Zugriff per API</LI>
				<LI><b>2,50 EUR / Monat / Ressource</b> welche mind. eines der obigen Features benötigt</LI>
			</UL>
		</Plan>
	</div>
</Section>

<Section side="right" title="In wenigen Schritten starten" id="getting-started" variant="highlighted">
	<P>
		<BookOpenPageVariantIcon class="float-right ml-4 text-[4em] text-accent-500" />
		Um mit sharePAD zu starten, müssen folgende Schritte durchgeführt werden. Das System läuft dabei
		vorerst in einem kostenfreien Demobetrieb. Die Benutzer sowie die Admins können so nach Belieben
		testen und sich mit dem System vertraut machen.
	</P>

	<UL>
		<LI>
			<b>eine Organisation/Gruppe <A href="https://app.sharepad.de/register">anlegen</A>.</b><br />
			HINWEIS: während die Reservierungsoberfläche sowohl auf Handy als auch PC/Tablet hervorragend funktioniert,
			wird für das Anlegen und Verwalten von sharePAD über die <A
				href="https://app.sharepad.de/admin">Adminoberfläche</A
			> ein PC/Tablet empfohlen.
		</LI>
		<LI>
			<b>Optional: die Benutzer vorab informieren.</b><br />
			Die Benutzer sollten frühzeitig von der Umstellung erfahren. Es empfiehlt sich ihnen vorab <A
				href="https://www.youtube.com/watch?v=EbiKOrDU5_s">den Einführungs&shy;screencast</A
			>
			zu schicken.
		</LI>
		<LI>
			<b>Einpflegen der Daten.</b><br />
			Für Organisationen die von elkato migrieren gibt es hierfür eine
			<A href="elkato-migration.pdf">ausführliche Migrationsanleitung</A>.<br />
			Für neue Organisationen sind folgende Schritte notwendig:
			<UL>
				<LI><b>In der Adminoberfläche alle Ressourcen anlegen.</b></LI>
				<LI>
					<b>In der Adminoberfläche alle Benutzer anlegen.</b><br />
					Diese bekommen dabei automatisch eine Einladungsmail in der sie auch ihre Passwörter vergeben
					können.<br />
					ACHTUNG: Bei der automatischen Migration von elkato wird das elkato-Passwort übernommen, weshalb
					auch keine Einladungsmails an die migrierten Nutzer versendet werden.
				</LI>
			</UL>
		</LI>
		<LI>
			<b>In den Produktivbetrieb wechseln</b><br />
			Um dann in den Produktivbetrieb zu wechseln muss in der Adminoberfläche unter "Einstellungen" der
			entsprechende Button geklickt werden. <br />
			ACHTUNG: elkato-Nutzer müssen vorher nocheinmal migrieren um auch wirklich den aktuellen Stand
			in sharePAD zu haben.
		</LI>
	</UL>
</Section>

<Section side="left" title="Für Entwickler: sharePAD erweitern" id="extend-sharepad">
	<P>
		Wer sehr spezielle Erweiterungswünsche für sharePAD hat, dem stellt sharePAD auch eine
		Erweiterungsschnittstelle (ein sogananntes API) zur Verfügung. Notwendig dazu ist eine
		EntwicklerIn (z.B. aus der Organisation) die die Funktionalität umsetzt und hierzu über das API
		auf die Daten von sharePAD zugreift.
	</P>
	<P>
		Das API ist unter <A href="https://beta.sharepad.de/docs">https://app.sharepad.de/docs</A>
		dokumentiert. Um darauf zuzugreifen wird ein sogenannter API Key benötigt. Wie dieser erstellt wird
		ist <A href="https://www.youtube.com/watch?v=9vgOzmRG4To">hier</A>
		dokumentiert.
	</P>
	<P>
		Zu beachten ist, daß die API nur für Pro-Benutzer (siehe <A href="#pricing">Preise</A>) zur
		Verfügung steht!
	</P>
</Section>

<!-- Footer -->
<footer class="relative bg-gradient-to-br from-warm-100 to-warm-200 pt-16 pb-8">
	<!-- Decorative wave SVG -->
	<svg class="absolute -top-1 left-0 w-full h-16 text-white" preserveAspectRatio="none" viewBox="0 0 1440 54">
		<path fill="currentColor" d="M0 22L60 16.7C120 11 240 1 360 0.7C480 1 600 11 720 16.7C840 22 960 22 1080 18.3C1200 15 1320 7 1380 3.5L1440 0V54H1380C1320 54 1200 54 1080 54C960 54 840 54 720 54C600 54 480 54 360 54C240 54 120 54 60 54H0V22Z"></path>
	</svg>

	<div class="mx-auto max-w-6xl px-6">
		<div class="grid grid-cols-1 md:grid-cols-3 gap-12 mb-12">
			<!-- Brand column -->
			<div>
				<div class="text-2xl font-bold mb-4">
					<span class="text-gradient">share</span><span class="text-gradient-blue">PAD</span>
				</div>
				<p class="text-warm-600 text-sm">
					Die Plattform für gemeinschaftliche Ressourcennutzung. Einfach, fair, verbindend.
				</p>
			</div>

			<!-- Quick links -->
			<div>
				<h4 class="font-semibold text-warm-800 mb-4">Schnellzugriff</h4>
				<ul class="space-y-2 text-sm">
					<li><a href="#intro" class="text-warm-600 hover:text-primary-600 transition-colors">So funktioniert's</a></li>
					<li><a href="#pricing" class="text-warm-600 hover:text-primary-600 transition-colors">Preise</a></li>
					<li><a href="#getting-started" class="text-warm-600 hover:text-primary-600 transition-colors">Erste Schritte</a></li>
					<li><a href="https://app.sharepad.de" class="text-warm-600 hover:text-primary-600 transition-colors">Zur App</a></li>
				</ul>
			</div>

			<!-- Contact & Legal -->
			<div>
				<h4 class="font-semibold text-warm-800 mb-4">Kontakt & Rechtliches</h4>
				<ul class="space-y-2 text-sm">
					<li><a href="mailto:info@sharepad.de" class="text-warm-600 hover:text-primary-600 transition-colors">info@sharepad.de</a></li>
					<li><a href="/site/impressum" class="text-warm-600 hover:text-primary-600 transition-colors">Impressum</a></li>
					<li><a href="Datenschutzerklärung.pdf" class="text-warm-600 hover:text-primary-600 transition-colors">Datenschutzerklärung</a></li>
				</ul>
			</div>
		</div>

		<!-- Bottom bar -->
		<div class="border-t border-warm-300 pt-6 flex flex-col sm:flex-row justify-between items-center gap-4 text-sm text-warm-500">
			<span>&copy; {new Date().getFullYear()} sharePAD. Alle Rechte vorbehalten.</span>
			<span>Mit Liebe gemacht für Communities</span>
		</div>
	</div>
</footer>

<script>
	import AccountQuestionIcon from 'svelte-material-icons/AccountQuestion.svelte';
	import CalendarClockIcon from 'svelte-material-icons/CalendarClock.svelte';
	import CashMultipleIcon from 'svelte-material-icons/CashMultiple.svelte';
	import BookOpenPageVariantIcon from 'svelte-material-icons/BookOpenPageVariant.svelte';
	import ChevronDoubleDownIcon from 'svelte-material-icons/ChevronDoubleDown.svelte';
	import P from '$lib/ui/p.svelte';
	import UL from '$lib/ui/ul.svelte';
	import LI from '$lib/ui/li.svelte';
	import A from '$lib/ui/a.svelte';
	import Section from '$lib/ui/section.svelte';
	import Plan from '$lib/ui/plan.svelte';
	import Badge from '$lib/ui/badge.svelte';
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';

	let topOfPage = $state(true);

	onMount(() => {
		topOfPage = window.scrollY === 0;
		window.onscroll = () => {
			topOfPage = window.scrollY === 0;
		};

		// Scroll animation observer
		const observerOptions = {
			threshold: 0.1,
			rootMargin: '0px 0px -50px 0px'
		};

		const observer = new IntersectionObserver((entries) => {
			entries.forEach(entry => {
				if (entry.isIntersecting) {
					entry.target.classList.add('visible');
				}
			});
		}, observerOptions);

		// Observe all sections for scroll animation
		document.querySelectorAll('section').forEach(section => {
			section.classList.add('animate-on-scroll');
			observer.observe(section);
		});

		return () => observer.disconnect();
	});
</script>
