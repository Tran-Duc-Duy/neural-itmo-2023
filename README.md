# Emotion Detect - Nhận diện cảm xúc

## Đôi lời phát biểu:

Trong quá trình học môn học neural thì Duy phải học khá nhiều thứ về deep learning, tuy nhiên giáo yêu cầu phải làm một project ứng dụng được vào cuộc sống, Duy và nhóm có Hải, Lãm đã triển khai ra ứng dụng nhận diện cảm xúc thông qua khuôn mặt với CNN, và thông qua âm thanh với RNN. Ứng dụng này quay video màn hình và hỗ trợ các video call nhận diện rằng đối phương đang vui hay buồn, sau này sẽ thêm phần gợi ý những câu nói cho người hướng nội, tuy nhiên ở phạm vi học tập, chúng tôi chỉ làm đến giai đoạn vui chơi giải trí, nhận diện cho vui nhà vui cửa, còn làm cho đến hết hay không thì còn tùy xem còn thời gian học.

## Hướng dẫn sử dụng trước khi dùng:

1. Clone dự án:

```shell
git clone https://github.com/Tran-Duc-Duy/neural-itmo-2023.git
```

2. Sử dụng với docker:

```shell
docker-compose up
```

Sử dụng với XAMPP thì nó dễ hơn, mở XAMPP lên rồi mở mysql lên là xong.

3. Chạy dự án:

```shell
py main.py
```

4. Nếu muốn hỗ trợ chỉnh sửa:

```
1. Tiến hành chỉnh sửa UI trong QT creator
2. Nhớ chuyển đổi UI thành py: pyside6-uic main.ui> modules/main_ui.py
3. Rồi, vào cmd chạy: py main.py

```

Okey - ứng dụng cơ bản đơn giản dễ hiểu, mong là sẽ được cho vài \* lấy động lực full source code hehe ))
