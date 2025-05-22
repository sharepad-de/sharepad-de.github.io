<li
	class="relative mt-2 mb-2 pl-6 before:absolute before:left-0 before:text-xl before:font-bold before:text-orange-400 before:content-['✓']"
>
	{@render children()}
</li>

<script>
	let { children } = $props();
</script>
