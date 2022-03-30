import { defineStore } from "pinia";

import { useProjectStore } from "@/stores/project";
import DocumentsApi from "@/utilities/network/document";

export const useDetailedDocumentStore = defineStore({
  id: "detailedDocument",
  state: () => ({
    document: null,
    maxWords: 50,
  }),
  getters: {
    getDocument: (state) => {
      return state.document;
    },
    getMaxWords: (state) => {
      return state.maxWords;
    },
  },
  actions: {
    fetchDocument(docID) {
      const projectStore = useProjectStore();
      return DocumentsApi.detailedDocument(
        projectStore.getProjectInfo.id,
        docID
      ).then((res) => {
        const sortedScores = {};
        for (let word of res.words) {
          const scores = {};
          for (let score of word.word_annotation_score) {
            scores[score.annotation] = score;
            if (!(score.annotation in sortedScores)) {
              sortedScores[score.annotation] = [];
            }
            sortedScores[score.annotation].push([score.score, score]);
          }
          word["scores"] = scores;
          delete word.word_annotation_score;
        }
        for (let key in sortedScores) {
          const scores = sortedScores[key];
          scores.sort((a, b) => {
            return b[0] - a[0];
          });
          let lastRank = 0;
          for (let index = 0; index < scores.length; index++) {
            const element = scores[index];
            if (index > 0 && scores[index - 1][0] !== element[0]) {
              lastRank = index;
            }
            element[1]["order"] = lastRank;
          }
        }
        this.document = res;
        // this.maxWords = res.words.length;
      });
    },
  },
});
