/**
 * services/documents.js
 * ------------------------
 * Wraps every document/analysis endpoint from Module 25's API design.
 */
import api from "./api";

export const uploadDocument = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/documents/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const listDocuments = () => api.get("/documents");
export const getDocument = (id) => api.get(`/documents/${id}`);
export const deleteDocument = (id) => api.delete(`/documents/${id}`);

export const analyzeDocument = (id, language = "en") =>
  api.post(`/documents/${id}/analyze`, { language });

export const getAnalysis = (id) => api.get(`/documents/${id}/analysis`);
export const getRisks = (id) => api.get(`/documents/${id}/risks`);
export const getEvidence = (id) => api.get(`/documents/${id}/evidence`);
export const getTranslation = (id, language) =>
  api.get(`/documents/${id}/translation`, { params: { language } });
export const getReport = (id) => api.get(`/documents/${id}/report`);
