<template>
  <p v-if="!textbook">Loading...</p>

  <div v-else>
    <PageHeader :pageTitle="textbook.title" />

    <!-- when Tabs emits the onSelectedTab event, take its tabTitle and set selectedTab state to this string value -->
    <Tabs
      :tabs="tabs"
      :selectedTab="selectedTab"
      @onSelectTab="selectedTab = $event"
    />
    <!-- TODO make this lessons listing into its own component -->
    <div class="lessons" v-if="selectedTab === 'Lessons'">
      <div
        class="row"
        v-for="lesson in textbook.lessons"
        :key="lesson.id"
        v-once
      >
        <!-- TODO is subtitle calc too much? should this be a map?-->
        <Expandable
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
          <p>text</p>
        </Expandable>
      </div>
    </div>
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
import PageHeader from "@/components/PageHeader.vue"; // @ is an alias to /src
import Tabs from "@/components/Tabs.vue";
import Expandable from "@/components/Expandable.vue";
import store from "@/store";

export default defineComponent({
  name: "CourseDashboard",
  components: {
    PageHeader,
    Tabs,
    Expandable,
  },
  setup() {
    const tabs = [
      { ionIconName: "book-outline", tabTitle: "Lessons" },
      { ionIconName: "briefcase-outline", tabTitle: "Resources" },
      { ionIconName: "clipboard-outline", tabTitle: "Project" },
    ];

    // the default tab is always Lessons
    const state = reactive({
      selectedTab: "Lessons",
    });

    store.dispatch("getDigitalStewardTextbook");
    const textbook = computed(() => store.state.textbook);

    // We want to expand the first incomplete lesson, so find its ID
    const defaultExpandedId = computed(
      () => textbook.value?.lessons?.find((lesson) => !lesson.completed)?.id
    );

    return { tabs, ...toRefs(state), textbook, defaultExpandedId };
  },
});
</script>
