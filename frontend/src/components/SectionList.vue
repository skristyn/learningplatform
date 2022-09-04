<template>
  <ul class="sectionList">
    <li class="row" v-for="section in sections" :key="section.id" v-once>
      <!-- <router-link :to="{ name: 'LessonIntro', params: { id: section.id } }">
      </router-link> -->
      <ion-icon
        :name="
          section.completed ? 'checkmark-circle-outline' : 'ellipse-outline'
        "
        :class="{ complete: section.completed }"
      ></ion-icon>
      <div class="underlined">
        <p class="title">
          Section {{ section.section_num }}: {{ section.title }}
        </p>
        <ion-icon name="time"></ion-icon>
        <p
          v-text="
            section.time_to_complete < 60
              ? `${section.time_to_complete} minutes`
              : `${section.time_to_complete / 60} hours`
          "
        ></p>
      </div>
    </li>
  </ul>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { Section } from "@/types/Textbook";

export default defineComponent({
  name: "SectionList",
  components: {},
  props: {
    sections: {
      type: Array as PropType<Section[]>,
    },
  },
});
</script>

<style scoped>
.sectionList {
  color: var(--var-color-gray);
  padding: 30px 14px;
  margin: 0;
}

p {
  margin: 0;
}

.row {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.title {
  font-size: 17px;
  font-weight: 500;
  margin-right: 16px;
}

.underlined {
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--var-color-gray);
  padding: 4px 30px 4px 0;
}

ion-icon {
  font-size: 22px;
  --ionicon-stroke-width: 60px;
  margin-right: 6px;
}

ion-icon.complete {
  color: var(--var-color-green);
}
</style>
