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
      <DButton
        size="large"
        text="Begin Lesson!"
        :to="{ name: 'Lesson', params: { sectionId: section.id } }"
      />
    </div>
  </div>
</template>

<script lang="ts">
import store from "@/store";
import { computed, defineComponent } from "vue";
import PageHeader from "@/components/PageHeader.vue";
import DButton from "@/components/DButton.vue"; // @ is an alias to /src

export default defineComponent({
  name: "LessonIntro",
  components: {
    PageHeader,
    DButton,
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
</style>
