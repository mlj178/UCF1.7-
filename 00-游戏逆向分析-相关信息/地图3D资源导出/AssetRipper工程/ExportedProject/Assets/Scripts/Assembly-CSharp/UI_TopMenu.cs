using UnityEngine;
using UnityEngine.UI;

public class UI_TopMenu : Singleton<UI_TopMenu>
{
	public enum Frame
	{
		GameRoom = 0,
		Inven = 1
	}

	[SerializeField]
	private AudioClip[] music;

	[SerializeField]
	private AudioSource bgmSource;

	[SerializeField]
	private Button[] changeFrameBtns;

	private Frame curFrame;

	protected override void Awake()
	{
	}

	public void OnMediaBtnDown()
	{
	}

	public void OnInvenBtnDown()
	{
	}

	public void OnBackBtnDown()
	{
	}

	public void ChangeFrame(Frame newFrame)
	{
	}

	private void SetFrameVisible(Frame frame, bool visible)
	{
	}

	private void PlayBGM(int index)
	{
	}
}
