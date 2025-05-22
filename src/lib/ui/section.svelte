<div
	{id}
	class="m-10 text-gray-600 sm:w-md md:w-1/2"
	class:sm:mr-auto={side === 'left'}
	class:sm:ml-auto={side === 'right'}
>
	<h2 class="mt-10 text-4xl font-bold text-orange-400">
		{title}
	</h2>
	{@render children()}
</div>

<script>
	let { children, title, side, id } = $props();
</script>
