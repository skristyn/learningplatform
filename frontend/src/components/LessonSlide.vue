<template>
  <!-- TODO verify that these layouts match the intention of the 'types' -->
  <div v-if="slide.type === 'headlineleftimage'" class="headlineleftimage">
    <!-- TODO verify if any other layouts can have an image -->
    <img :src="image_src" />
    <div>
      <h2 v-if="slide?.value.heading">
        {{ slide.value.heading }}
      </h2>
      <span v-html="slide?.value.body"></span>
    </div>
  </div>
</template>

<script lang="ts">
import { Slide } from "@/types/Section";
import SlideImage from "@/types/SlideImage";
import { computed, defineComponent, PropType } from "vue";

export default defineComponent({
  name: "LessonSlide",
  props: {
    slide: {
      type: Object as PropType<Slide>,
      required: true,
    },
    image: {
      type: Object as PropType<SlideImage | null>,
      required: true, // TODO verify that slides always have an image
    },
    // currentIndex: {
    //   type: Number,
    //   required: true,
    //   default: 0,
    // },
  },
  setup(props) {
    const image_src = computed(
      // TODO update this URL when the files are hosted elsewhere
      () => "http://localhost:8000" + props.image?.meta.download_url
    );

    return { image_src };
  },
});
</script>

<style scoped>
/* Scoped styles go here --- These only apply to ids and classes in this file*/
.headlineleftimage {
  display: flex;
  flex-flow: row nowrap;
}

.headlineleftimage img {
  margin-right: 30px;
}
</style>
