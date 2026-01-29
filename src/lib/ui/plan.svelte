<div
	class="relative glass rounded-3xl overflow-hidden transition-all duration-300 hover:-translate-y-1 hover:shadow-xl {defaultClass} {recommended ? 'ring-2 ring-primary-500 ring-offset-2' : ''}"
>
	<!-- Recommended badge -->
	{#if recommended}
		<div class="absolute -top-1 -right-1 z-10">
			<div class="bg-gradient-to-r from-primary-500 to-primary-600 text-white text-xs font-bold px-3 py-1 rounded-bl-xl rounded-tr-2xl shadow-md">
				Empfohlen
			</div>
		</div>
	{/if}

	<!-- Gradient header -->
	<div
		class="p-4 pl-6 text-xl font-bold text-white"
		class:bg-gradient-to-r={true}
		class:from-accent-400={light}
		class:to-accent-500={light}
		class:from-accent-600={!light}
		class:to-accent-700={!light}
	>
		{title}
	</div>

	<!-- Content -->
	<div class="p-2">
		{@render children()}
	</div>

	<!-- CTA Button -->
	{#if cta}
		<div class="px-6 pb-6">
			<a
				href={ctaHref || '#'}
				class="block w-full text-center py-3 px-6 rounded-xl font-semibold transition-all duration-300 {light ? 'bg-accent-100 text-accent-700 hover:bg-accent-200' : 'bg-gradient-to-r from-primary-500 to-primary-600 text-white hover:from-primary-600 hover:to-primary-700 shadow-md hover:shadow-lg'}"
			>
				{cta}
			</a>
		</div>
	{/if}
</div>

<script>
	let {
		children,
		title,
		light = false,
		recommended = false,
		cta = undefined,
		ctaHref = undefined,
		class: defaultClass = ''
	} = $props();
</script>
