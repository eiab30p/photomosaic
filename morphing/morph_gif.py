import imageio

dst1 = cv2.addWeighted(img, 0.9, img2, 0.1, 0)
dst2 = cv2.addWeighted(img, 0.8, img2, 0.2, 0)
dst3 = cv2.addWeighted(img, 0.7, img2, 0.3, 0)
dst4 = cv2.addWeighted(img, 0.6, img2, 0.4, 0)
dst5 = cv2.addWeighted(img, 0.5, img2, 0.5, 0)
dst6 = cv2.addWeighted(img, 0.4, img2, 0.6, 0)
dst7 = cv2.addWeighted(img, 0.3, img2, 0.7, 0)
dst8 = cv2.addWeighted(img, 0.2, img2, 0.8, 0)
dst9 = cv2.addWeighted(img, 0.1, img2, 0.9, 0)

images = [dst1,dst2, dst3, dst4, dst5, dst6, dst7, dst8, dst9,dst9, dst9, dst8,dst7, dst6, dst5, dst4, dst3, dst2, dst1, dst1, dst1]
imageio.mimsave('morph.gif', images)