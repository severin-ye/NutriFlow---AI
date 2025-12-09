import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  model: "gpt-4o-mini",
});

export async function analyzeWithLangChain(base64Image) {
  const response = await model.invoke([
    {
      role: "user",
      content: [
        { type: "text", text: "Describe and analyze this image." },
        {
          type: "image_url",
          image_url: `data:image/jpeg;base64,${base64Image}`,
        },
      ],
    },
  ]);

  return response?.content;
}

