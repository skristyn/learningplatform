<template>
  <p v-if="!textbook">Loading...</p>

  <div v-else>
    <DPageHeader :title="textbook.title" />

    <div class="nextUpContainer">
      <DButton
        size="small"
        :text="`Continue Lesson ${nextUp.lesson?.lesson_num}.${nextUp.section?.section_num}: ${nextUp.section?.title}`"
        :to="{
          name: 'LessonIntro',
          params: {
            lessonId: nextUp.lesson?.id,
            sectionId: nextUp.section?.id,
          },
        }"
      />
    </div>

    <DProgressBar title="Your Progress" :percentComplete="percentComplete" />

    <!-- when DTabs emits the onSelectedTab event, take its tabTitle and set selectedTab state to this string value -->
    <DTabs
      :tabs="tabs"
      :selectedTab="selectedTab"
      @onSelectTab="selectedTab = $event"
    />

    <!-- One of the following three will display based on tab selection -->
    <LessonList v-if="selectedTab === 'Lessons'" :lessons="textbook.lessons" />
    <div v-if="selectedTab === 'Resources'">
      <p>resources placeholder</p>
    </div>
    <div v-if="selectedTab === 'Project'">
      <p>project placeholder</p>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, reactive, toRefs } from "vue";
import DPageHeader from "@/components/DPageHeader.vue"; // @ is an alias to /src
import DTabs from "@/components/DTabs.vue";
import store from "@/store";
import LessonList from "@/components/LessonList.vue";
import DProgressBar from "@/components/DProgressBar.vue";
import DButton from "@/components/DButton.vue";

export default defineComponent({
  name: "CourseDashboard",
  components: {
    DPageHeader,
    DTabs,
    LessonList,
    DProgressBar,
    DButton,
  },
  setup() {
    const tabs = [
      { ionIconName: "book-outline", tabTitle: "Lessons" },
      // TODO uncomment these lines once the Resrouces and Projects endpoints are ready & populated
      // { ionIconName: "briefcase-outline", tabTitle: "Resources" }, // currently not populated with data
      // { ionIconName: "clipboard-outline", tabTitle: "Project" }, // endpoint is still in the works
    ];

    // the default tab is always Lessons
    const state = reactive({
      selectedTab: "Lessons",
    });

    store.dispatch("getDigitalStewardTextbook");
    const textbook = computed(() => store.state.textbook);

    // calculate their progress through the textbook
    const percentComplete = computed(() => {
      const sectionCounts = store.state.textbook?.lessons?.reduce(
        ({ completed, total }, lesson) => {
          const completedSectionCount = lesson.sections.filter(
            (section) => section.completed
          ).length;
          const totalSectionCount = lesson.sections.length;

          return {
            completed: completed + completedSectionCount,
            total: total + totalSectionCount,
          };
        },
        { completed: 0, total: 0 }
      );

      // if an error occured and the textbook didn't return any sections, default to 0% complete
      if (!sectionCounts?.total) {
        return 0;
      }

      // ... otherwise, calculate % complete
      const percentComplete =
        (sectionCounts?.completed / sectionCounts?.total) * 100;

      return percentComplete;
    });

    // find the first undone lesson and section (we want a quick link to this)
    const nextUp = computed(() => {
      const lesson = store.state.textbook?.lessons?.find(
        (lesson) => !lesson.completed
      );

      const section = lesson?.sections.find((section) => !section.completed);

      return { lesson, section };
    });

    return {
      tabs,
      ...toRefs(state),
      textbook,
      percentComplete,
      nextUp,
    };
  },
});
</script>

<style scoped>
.nextUpContainer {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 40px;
  margin-top: 100px;
}
</style>
