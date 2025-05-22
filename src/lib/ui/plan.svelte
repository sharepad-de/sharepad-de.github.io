<div
	class="rounded-2xl border shadow-lg {defaultClass}"
	class:border-blue-300={light}
	class:border-blue-500={!light}
>
	<div
		class="overflow-clip rounded-t-2xl p-1 pl-5 text-xl font-bold text-white"
		class:bg-blue-300={light}
		class:bg-blue-500={!light}
	>
		{title}
	</div>
	{@render children()}
</div>

<script>
	let { children, title, light = undefined, class: defaultClass } = $props();
</script>
