<ul class="mt-4 mb-6 {defaultClass}">
	{@render children()}
</ul>

<script>
	let { children, class: defaultClass = '' } = $props();
</script>
