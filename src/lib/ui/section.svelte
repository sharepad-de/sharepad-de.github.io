<section
	{id}
	class="relative py-16 md:py-24 {variant === 'highlighted' ? 'bg-warm-50' : ''} {variant === 'card' ? 'bg-gradient-to-br from-warm-50 to-primary-50/30' : ''}"
>
	<!-- Decorative divider line at top -->
	<div class="absolute top-0 left-1/2 -translate-x-1/2 w-24 h-1 bg-gradient-to-r from-primary-400 via-primary-500 to-primary-400 rounded-full"></div>

	<div
		class="mx-auto max-w-4xl px-6 md:px-10 text-warm-700 text-left"
		class:md:mr-auto={side === 'left'}
		class:md:ml-auto={side === 'right'}
	>
		<h2 class="relative inline-block mt-6 mb-8 text-3xl md:text-4xl font-bold text-warm-800">
			{title}
			<!-- Gradient underline accent -->
			<span class="absolute -bottom-2 left-0 w-full h-1 bg-gradient-to-r from-primary-400 to-primary-600 rounded-full"></span>
		</h2>
		<div class="text-warm-600 leading-relaxed">
			{@render children()}
		</div>
	</div>
</section>

<script>
	let { children, title, side = 'left', id = undefined, variant = 'default' } = $props();
</script>
