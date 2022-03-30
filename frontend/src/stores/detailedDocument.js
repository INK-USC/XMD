import { defineStore } from "pinia";

import { useProjectStore } from "@/stores/project";
import DocumentsApi from "@/utilities/network/document";

export const useDetailedDocumentStore = defineStore({
  id: "detailedDocument",
  state: () => ({
    document: null,
  }),
  getters: {
    getDocument: (state) => {
      return state.document;
    },
  },
  actions: {
    fetchDocument(docID) {
      const projectStore = useProjectStore();
      return DocumentsApi.detailedDocument(
        projectStore.getProjectInfo.id,
        docID
      ).then((res) => {
        for (let word of res.words) {
          const scores = {};
          for (let score of word.word_annotation_score) {
            scores[score.annotation] = score;
          }
          word["scores"] = scores;
          delete word.word_annotation_score;
        }
        this.document = res;
      });
    },
  },
});
