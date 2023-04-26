<template>
  <!-- TODO verify that there aren't any other possible layout 'type's -->
  <!-- TODO verify that these layouts match the intention of the 'type's -->
  <!-- TODO verify if any other layouts can have a heading -->
  <div
    v-if="slide.type === 'headlineleftimage'"
    class="fadeIn headlineleftimage"
  >
    <img class="slideImage" :src="image_src" :alt="image?.title" />
    <div>
      <h2 v-if="slide?.value.heading">
        {{ slide.value.heading }}
      </h2>
      <span v-html="slide?.value.body"></span>
    </div>
  </div>

  <div
    v-else-if="slide.type === 'imagerightblock'"
    class="fadeIn imagerightblock"
  >
    <div>
      <span v-html="slide?.value.body"></span>
    </div>
    <img class="slideImage" :src="image_src" :alt="image?.title" />
  </div>

  <div v-else-if="slide.type === 'imagetopblock'" class="fadeIn imagetopblock">
    <img class="slideImage" :src="image_src" :alt="image?.title" />
    <div>
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
  },
  setup(props) {
    const image_src = computed(
      // TODO update this URL when the files are hosted elsewhere
      () => "http://ugly.photography" + props.image?.meta.download_url
    );

    return { image_src };
  },
});
</script>

<style scoped>
/* Scoped styles go here --- These only apply to ids and classes in this file*/
.headlineleftimage,
.imagerightblock,
.imagetopblock {
  margin-bottom: 20px;
  height: 100%;
  overflow-y: auto;
}

.headlineleftimage,
.imagerightblock {
  display: flex;
  flex-flow: row nowrap;
}

.imagetopblock {
  display: flex;
  flex-flow: column nowrap;
}

.headlineleftimage img {
  margin-right: 30px;
}

.imagerightblock img {
  margin-left: 30px;
}

/* styles to fade in the slides */
.fadeIn {
  animation: fadeIn 0.4s;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
