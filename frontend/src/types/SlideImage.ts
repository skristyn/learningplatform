export default interface SlideImage {
  id: number;
  meta: {
    type: string;
    detail_url: string;
    tags: string[]; // TODO make sure the type of the array items is indeed string
    download_url: string;
  };
  title: string;
}
