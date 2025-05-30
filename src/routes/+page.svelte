<!-- Title Section -->
<div class="relative z-20 h-[80lvh] md:h-[70lvh] lg:h-[60lvh]">
	<div class="relative p-10 text-right sm:absolute sm:top-0 sm:right-0 md:pr-15">
		<div class="text-[13vw] font-bold sm:text-[10vw]">
			<span class="text-orange-400">share</span><span class="text-blue-600"><span>PAD</span> </span>
		</div>
		<div class="ml-auto w-1/2 text-xl font-bold text-gray-400">
			Die App, um die gemeinsame Nutzung von Autos, Lastenrädern und mehr zu organisieren
		</div>
	</div>
	<img
		src="mobile-with-app.png"
		alt="Phone with sharePAD App"
		class="-mt-20 h-[45lvh] pl-10 sm:absolute sm:mt-0 sm:h-auto sm:w-[50%] sm:pt-32 md:h-[75lvh] md:w-auto lg:pl-32"
	/>
</div>

<!-- Hoping Arrow symbol -->
{#if topOfPage}
	<a
		class="fixed right-8 bottom-8 z-50 animate-bounce rounded-[2em] border-[.4em] border-white bg-orange-400 p-2 text-xl font-bold text-white active:right-9"
		href="https://app.sharepad.de"
		transition:fade
	>
		Login
	</a>

	<ChevronDoubleDownIcon
		class="px-auto fixed bottom-3 z-40 w-full animate-pulse text-[6em] text-white"
	/>
{/if}

<!-- Transition-Image to first Section -->
<div class="relative">
	<img src="hero-background.png" alt="Menschen um Auto und Lastenrad" class="w-screen" />
	<div class="absolute top-0 right-0 left-0 h-1/2 bg-gradient-to-b from-white/100 to-white/0"></div>
</div>

<Section side="left" title="Was genau ist sharePAD?" id="intro">
	<P>
		<CalendarClockIcon class="float-right ml-4 text-[6em] text-blue-500" />
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
			<span class="italic">
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

<Section side="right" title="Für wen ist sharePAD?" id="audience">
	<P>
		<AccountQuestionIcon class="float-right ml-4 text-[6em] text-blue-500" />
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
		<CashMultipleIcon class="float-left mr-4 text-[4em] text-blue-500" />
		Für <em>jede Ressource</em> muss jeweils einer der folgenden Tarife gewählt werden. D.h.
		innerhalb einer Organisation können die beiden Tarife beliebig kombiniert werden. Man zahlt also
		nur, was man braucht. Eine Ressource kann zu einem späteren Zeitpunkt auch jederzeit von
		<em>Free</em> zu <em>Pro</em> geupgradet werden.
	</P>

	<div class="flex w-full flex-row flex-wrap gap-5">
		<Plan title="Free" light class="flex-1 xl:max-w-1/3">
			<UL class="m-5 text-left">
				<LI>beliebig viele Ressourcen</LI>
				<LI>beliebig viele Nutzer</LI>
				<LI>beliebig viele Reservierungen</LI>
				<LI>beliebig viele Partner&shy;organisationen</LI>
				<LI><b>kostenlos</b></LI>
			</UL>
		</Plan>

		<Plan title="Pro" class="flex-1 xl:max-w-1/3">
			<div class="m-5 mb-0">Alles wie in <b>Free</b> plus:</div>
			<UL class="m-5 text-left">
				<LI>Datenexport für Abrechnung</LI>
				<LI>Anbindung an Zutritts&shy;kontroll&shy;system <br /><em>(sobald verfügbar)</em></LI>
				<LI>Anbindung an elektronisches Fahrtenbuch <br /><em>(sobald verfügbar)</em></LI>
				<LI><b>2,50 EUR / Monat / Ressource</b> welche mind. eines der obigen Features benötigt</LI>
			</UL>
		</Plan>
	</div>
</Section>

<Section side="right" title="Los geht's..." id="getting-started">
	<P>
		<BookOpenPageVariantIcon class="float-right ml-4 text-[4em] text-blue-500" />
		Um mit sharePAD zu starten, müssen folgende Schritte durchgeführt werden. Zusätzlich gibt es für
		elkato-Nutzer eine
		<A href="elkato-migration.pdf">ausführliche Migrationsanleitung</A>.
	</P>

	<UL>
		<LI>
			eine Organisation/Gruppe <A href="https://app.sharepad.de/register">anlegen</A>.<br />
			<em
				>Hinweis: während die Reservierungsoberfläche sowohl auf Handy als auch PC/Tablet
				hervorragend funktioniert, wird für das Anlegen und Verwalten von sharePAD über die <A
					href="https://app.sharepad.de/admin">Adminoberfläche</A
				> ein PC/Tablet empfohlen.</em
			>
		</LI>
		<LI>
			Optional: die Benutzer vorab informieren, dass das Reservierungssystem eingerichtet wurde.
			Ggf. kann auch
			<A href="https://www.youtube.com/watch?v=EbiKOrDU5_s">der Einführungs&shy;screencast</A>
			mitgeschickt werden.
		</LI>
		<LI>In der Adminoberfläche alle Ressourcen anlegen</LI>
		<LI>
			In der Adminoberfläche alle Benutzer anlegen<br />
			(diese bekommen dabei automatisch eine Einladungsmail in der sie auch ihre Passwörter vergeben
			können).<br />Da es vorerst im Demobetrieb läuft können die Benutzer nach Belieben testen und
			sich mit dem System vertraut machen.
		</LI>
		<LI>
			Sobald sich alle das System angesehen haben kann der Regelbetrieb starten. Hierzu muss in der
			Adminoberfläche unter "Einstellungen" der entsprechende Button geklickt werden.
		</LI>
	</UL>
</Section>

<div
	class="border-t border-dashed border-orange-400 px-3 py-1 text-right font-bold text-orange-400"
>
	<a class="pl-3 sm:pl-10" href="Datenschutzerklärung.pdf">Datenschutzerklärung</a>
	<a class="pl-3 sm:pl-10" href="/site/impressum">Impressum</a>
	<a class="pl-3 sm:pl-10" href="mailto:info@sharepad.de">Kontakt</a>
</div>

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
	});
</script>
