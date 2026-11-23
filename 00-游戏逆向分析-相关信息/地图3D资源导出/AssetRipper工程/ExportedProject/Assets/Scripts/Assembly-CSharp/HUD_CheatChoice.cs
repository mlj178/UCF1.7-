using UnityEngine;
using UnityEngine.UI;

public class HUD_CheatChoice : RecyclableObject
{
	[SerializeField]
	private RectTransform rect;

	[SerializeField]
	private RawImage rawImg;

	[SerializeField]
	private Text choiceText;

	public bool isFocus
	{
		set
		{
		}
	}

	public void SetText(string str)
	{
	}

	public void SetPos(int pos)
	{
	}
}
