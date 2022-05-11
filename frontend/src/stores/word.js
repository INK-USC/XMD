import { defineStore } from "pinia";

import { useProjectStore } from "@/stores/project";
import WordsApi from "@/utilities/network/word";

export const useWordStore = defineStore({
  id: "words",
  state: () => ({
    words: [],
    curPage: 1,
    maxPage: 1,
    totalWordCount: 0,
    curWordIndex: 0,
    pageSize: 10,
    currDocuments: [],
    searchQuery: undefined,
  }),
  getters: {
    getWords: (state) => {
      return state.words;
    },
    getWordInfo: (state) => {
      return state;
    },
    getCurrWord: (state) => {
      return () => {
        return state.words[state.curWordIndex]
          ? state.words[state.curWordIndex].text
          : undefined;
      };
    },
    getDocuments: (state) => {
      return state.currDocuments;
    },
  },
  actions: {
    resetState(q = undefined) {
      this.curPage = 1;
      this.pageSize = 10;
      this.currDocuments = [];
      this.searchQuery = q;
      return this.fetchWords();
    },
    setCurWordIndex(curWordIndex) {
      this.curWordIndex = curWordIndex;
    },
    fetchWords() {
      const projectStore = useProjectStore();
      return WordsApi.list(
        projectStore.getProjectInfo.id,
        this.curPage,
        this.pageSize,
        this.searchQuery
      ).then((res) => {
        this.words = res.results;
        this.totalWordCount = res.count;
        this.maxPage = Math.ceil(this.totalWordCount / this.pageSize);
        return res;
      });
    },
    updateCurPage(newPageNum) {
      this.curPage = newPageNum;
      this.curWordIndex = 0;
      this.currDocuments = [];
      return this.fetchWords();
    },
    fetchDocuments() {
      const projectStore = useProjectStore();
      return WordsApi.documents(
        projectStore.getProjectInfo.id,
        this.getCurrWord()
      ).then((res) => {
        for (const doc of res.results) {
          // const sortedScores = {};
          for (let word of doc.words) {
            const scores = {};
            for (let score of word.word_annotation_score) {
              scores[score.annotation] = score;
              // if (!(score.annotation in sortedScores)) {
              //   sortedScores[score.annotation] = [];
              // }
              // sortedScores[score.annotation].push([score.score, score]);
            }
            word["scores"] = scores;
            delete word.word_annotation_score;
          }
          // for (let key in sortedScores) {
          //   const scores = sortedScores[key];
          //   scores.sort((a, b) => {
          //     return b[0] - a[0];
          //   });
          //   let lastRank = 0;
          //   for (let index = 0; index < scores.length; index++) {
          //     const element = scores[index];
          //     if (index > 0 && scores[index - 1][0] !== element[0]) {
          //       lastRank = index;
          //     }
          //     element[1]["order"] = lastRank;
          //   }
          // }
        }
        this.currDocuments = res.results;
      });
    },
  },
});
