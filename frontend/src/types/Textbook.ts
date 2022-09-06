export interface TextbookSection {
  id: number;
  title: string;
  description: string | null;
  completed: boolean;
  section_num: number;
  time_to_complete: number;
  detail_url: string;
}

export interface TextbookLesson {
  id: number;
  lesson_num: number;
  title: string;
  completed: boolean;
  time_remaining: number;
  detail_url: string;
  sections: TextbookSection[];
}

export default interface Textbook {
  id: number;
  meta: {
    type: string;
    detail_url: string;
  };
  title: string;
  description: string | null;
  lessons: TextbookLesson[];
  completed: boolean;
}
