using System;
using UnityEngine;
using UnityEngine.UI;

public class CommonHud_1 : MonoBehaviour
{
	[Serializable]
	public enum Type
	{
		Image = 0,
		RawImage = 1,
		Text = 2
	}

	[SerializeField]
	private Type graphicType;

	[SerializeField]
	private Image image;

	[SerializeField]
	private RawImage rawImage;

	[SerializeField]
	private Text text;

	public float fadeInTime;

	[SerializeField]
	public float normalTime;

	[SerializeField]
	public float fadeOutTime;

	private Color defaultColor;

	private Color zeroAlphaColor;

	private void Awake()
	{
	}

	public void Show(float inTime, float normalTime, float outTime)
	{
	}

	public void Show()
	{
	}

	private void EnterNormalState()
	{
	}

	private void EnterFadeOutState()
	{
	}

	public void SetGraphColor(Color color)
	{
	}

	public void SetSprite(Sprite spr)
	{
	}

	public void SetTexture(Texture tex)
	{
	}

	public void SetText(string msg)
	{
	}

	public void SetFontSize(int size)
	{
	}

	public void SetPos(Vector2 pos)
	{
	}

	public void SetTime(float inTime, float normalTime, float outTime)
	{
	}

	public void Shake(float duration)
	{
	}

	public void Shake(float duration, Vector2 originPos)
	{
	}

	public void Stop()
	{
	}
}
