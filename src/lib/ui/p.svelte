<div class="mt-6 mb-6 sm:text-justify leading-relaxed {highlight ? 'bg-primary-50/50 border-l-4 border-primary-400 pl-4 py-3 rounded-r-lg' : ''}">
	{@render children()}
</div>

<script>
	let { children, highlight = false } = $props();
</script>
