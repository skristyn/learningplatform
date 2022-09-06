export interface SectionLesson {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  section_num: number;
  time_to_complete: number;
  detail_url: string;
}

export default interface Lesson {
  id: number;
  meta: {
    type: string;
    detail_url: string;
  };
  title: string;
  description: string;
  number: number;
  completed: boolean;
  sections: SectionLesson[];
  time_remaining: number;
}
