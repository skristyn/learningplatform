<template>
  <div class="lessonList">
    <DExpandable
      v-for="lesson in lessons"
      :key="lesson.id"
      v-once
      :title="`Lesson ${lesson.lesson_num}: ${lesson.title}`"
      :subtitle="
        lesson.completed
          ? 'Complete!'
          : lesson.time_remaining < 60
          ? `${lesson.time_remaining} minutes`
          : `${lesson.time_remaining / 60} hours`
      "
      :subtitleIcon="lesson.completed ? '' : 'time'"
      :isExpanded="lesson.id == defaultExpandedId"
    >
      <!-- place the lesson's section list the expandable area -->
      <SectionList :sections="lesson.sections" :lessonId="lesson.id" />
    </DExpandable>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "vue";
import { TextbookLesson } from "@/types/Textbook";
import DExpandable from "@/components/DExpandable.vue";
import SectionList from "./SectionList.vue";

export default defineComponent({
  name: "LessonList",
  components: {
    DExpandable,
    SectionList,
  },
  props: {
    lessons: {
      type: Array as PropType<TextbookLesson[]>,
      required: true,
    },
  },
  setup(props) {
    // find the lesson id of the first incomplete lesson (we want it expanded by default)
    const defaultExpandedId = computed(
      () => props.lessons?.find((lesson) => !lesson.completed)?.id
    );

    return { defaultExpandedId };
  },
});
</script>

<style scoped>
.lessonList {
  padding: 24px 98px;
}
</style>
