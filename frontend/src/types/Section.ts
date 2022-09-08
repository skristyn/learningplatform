export interface Slide {
  type: "headlineleftimage" | "imagerightblock" | "imagetopblock"; // TODO make sure this is the full list of all possible 'type's
  value: {
    heading: string;
    body: string;
    image: number;
  };
  id: string;
  tips_url: string;
}

export default interface Section {
  id: number;
  meta: {
    type: string;
    detail_url: string;
  };
  title: string;
  description: string | null;
  lesson_id: number;
  lesson_url: string;
  number: number;
  time_to_complete: number;
  completed: boolean;
  slides: Slide[];
}
