using UnityEngine;
using UnityEngine.UI;

public class HUD_PlayerRect : RecyclableObject
{
	public enum Type
	{
		BL = 0,
		GR = 1,
		Dead = 2
	}

	[SerializeField]
	private RectTransform rect;

	[SerializeField]
	private Image image;

	[SerializeField]
	private Sprite[] asset;

	public void SetPos(int id, bool left)
	{
	}

	public void SetImage(Type type)
	{
	}
}
