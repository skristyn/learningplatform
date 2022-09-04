export interface Section {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  section_num: number;
  time_to_complete: number;
  detail_url: string;
}

export interface Lesson {
  id: number;
  lesson_num: number;
  title: string;
  completed: boolean;
  time_remaining: number;
  detail_url: string;
  sections: Section[];
}

export default interface Textbook {
  id: 4;
  meta: {
    type: string;
    detail_url: string;
  };
  title: string;
  description: string | null;
  lessons: Lesson[];
  completed: boolean;
}
