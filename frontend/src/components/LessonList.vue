<template>
  <div class="lessonList">
    <Expandable
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
    </Expandable>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "vue";
import { TextbookLesson } from "@/types/Textbook";
import Expandable from "@/components/Expandable.vue";
import SectionList from "./SectionList.vue";

export default defineComponent({
  name: "LessonList",
  components: {
    Expandable,
    SectionList,
  },
  props: {
    lessons: {
      type: Array as PropType<TextbookLesson[]>,
      required: true,
    },
  },
  setup(props) {
    // We want to expand the first incomplete lesson, so find its ID
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
