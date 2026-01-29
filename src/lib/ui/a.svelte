{#if variant === 'button'}
	<a
		{href}
		class="inline-block px-6 py-3 rounded-xl font-semibold transition-all duration-300 {primary ? 'bg-gradient-to-r from-primary-500 to-primary-600 text-white hover:from-primary-600 hover:to-primary-700 shadow-md hover:shadow-lg hover:-translate-y-0.5' : 'bg-warm-100 text-warm-700 hover:bg-warm-200 border border-warm-300'}"
	>
		{@render children()}
	</a>
{:else}
	<a
		{href}
		class="relative inline-block text-accent-600 font-medium transition-colors duration-200 hover:text-accent-700 group"
	>
		{@render children()}
		<!-- Animated underline -->
		<span class="absolute bottom-0 left-0 w-full h-0.5 bg-accent-400 origin-right scale-x-0 transition-transform duration-300 group-hover:origin-left group-hover:scale-x-100"></span>
	</a>
{/if}

<script>
	let { href, children, variant = 'link', primary = false } = $props();
</script>
