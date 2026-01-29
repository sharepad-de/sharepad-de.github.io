<span class="inline-flex items-center gap-1 mr-2 px-2 py-0.5 rounded-md text-xs font-semibold border {variantClasses[variant]}">
	{#if icon}
		{@const Icon = icon}
		<Icon class="w-3 h-3" />
	{/if}
	{title}
</span>

<script>
	const variantClasses = {
		planned: 'bg-accent-50 text-accent-700 border-accent-200',
		info: 'bg-warm-100 text-warm-700 border-warm-300',
		new: 'bg-green-50 text-green-700 border-green-200',
		pro: 'bg-primary-50 text-primary-700 border-primary-200'
	};

	let { title, variant = 'planned', icon = undefined } = $props();
</script>
