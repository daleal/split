<script setup lang="ts">
const props = defineProps<{ show: boolean }>();
</script>

<template>
  <Teleport to="body">
    <Transition
      enter-from-class="opacity-0"
      enter-active-class="transition duration-300"
      leave-to-class="opacity-0"
      leave-active-class="transition duration-300"
    >
      <div
        v-if="props.show"
        class="fixed left-0 top-0 z-50 w-screen h-screen"
      >
        <div
          class="
            flex overflow-hidden justify-center items-center
            h-full bg-black/30
          "
        >
          <div
            class="px-4 w-full min-w-fit max-w-fit h-auto mx-auto"
          >
            <div class="relative bg-white rounded-lg shadow">
              <div class="p-5 max-h-[85vh]">
                <slot />
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>
