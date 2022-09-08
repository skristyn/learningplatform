<template>
  <!-- TODO, you should be able to go to this page directly -->
  <p v-if="!textbookTitle || !lesson || !section">Loading...</p>
  <div v-else>
    <PageHeader
      :title="textbookTitle"
      :subtitle="`Lesson ${lesson.number}: ${lesson.title}`"
      :breadcrumbTitle="`Lesson ${lesson.number}.${section?.section_num}`"
    />
    <h2 class="sectionTitle">
      {{ `Section ${section.section_num} // ${section.title}` }}
    </h2>
    <p class="time">
      {{ `Estimated time: ${section.time_to_complete} minutes` }}
    </p>
    <!-- If the section has a description, display -->
    <div v-if="section.description" class="description">
      <h4>What you’ll learn</h4>
      <p>{{ section.description }}</p>
    </div>
    <div class="buttonContainer">
      <router-link
        class="button"
        :to="{ name: 'Lesson', params: { sectionId: section.id } }"
        >Begin Lesson!</router-link
      >
    </div>
  </div>
</template>

<script lang="ts">
import store from "@/store";
import { computed, defineComponent } from "vue";
import PageHeader from "@/components/PageHeader.vue"; // @ is an alias to /src

export default defineComponent({
  name: "LessonIntro",
  components: {
    PageHeader,
  },
  props: {
    lessonId: {
      type: Number,
      required: true,
    },
    sectionId: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    store.dispatch("getCurrentLesson", props.lessonId);

    const textbookTitle = computed(() => store.state.textbook?.title);

    const lesson = computed(() => store.state.currentLesson);

    const section = computed(() =>
      store.state.currentLesson?.sections.find(
        (section) => section.id === +props.sectionId // cast sectionId prop to a number
      )
    );

    return { textbookTitle, lesson, section };
  },
});
</script>

<style scoped>
.sectionTitle {
  background-color: var(--var-color-gray-lighter);
  padding: 12px 18px;
  margin: 0;
}

.time {
  border-bottom: 1px solid var(--var-color-gray);
  padding: 14px 18px 16px;
  margin: 0 0 42px;
}

.buttonContainer {
  display: flex;
  justify-content: center;
}

.button {
  display: inline-block; /* needed to add padding to this <a> tag */
  border: 2px solid red;
  border-radius: 10px;
  padding: 18px 96px;
  font-size: 26px;
  font-weight: bold;
}

.button:link,
.button:visited,
.button:hover,
.button:active {
  text-decoration: none;
  color: var(--var-color-almost-black);
}
</style>
