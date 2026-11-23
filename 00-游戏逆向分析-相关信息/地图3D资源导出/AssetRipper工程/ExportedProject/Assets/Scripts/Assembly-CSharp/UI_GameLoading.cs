using UnityEngine;
using UnityEngine.UI;

public class UI_GameLoading : Singleton<UI_GameLoading>
{
	[SerializeField]
	private RawImage loadingBG;

	[SerializeField]
	private Image gaugeImage;

	public static float progress
	{
		set
		{
		}
	}

	public static Texture loadingTex
	{
		set
		{
		}
	}
}
