<li class="relative mt-3 mb-3 pl-8">
	<!-- Gradient checkmark circle -->
	<span class="absolute left-0 top-0.5 flex items-center justify-center w-5 h-5 rounded-full bg-gradient-to-br from-primary-400 to-primary-600 text-white text-xs font-bold shadow-sm">
		&#10003;
	</span>
	{@render children()}
</li>

<script>
	let { children } = $props();
</script>
