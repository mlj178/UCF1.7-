using System;
using UnityEngine;

[Serializable]
public struct WpnSpriteAsset
{
	public Texture background;

	public Color backgroundColor;

	public Texture effect;

	public Texture line;

	public Texture select;

	public Texture select2;

	public Texture bagIcon;

	public Sprite killMsgIcon;

	public Sprite killMsgIcon2;

	public static WpnSpriteAsset Null;

	public void GetBigIcon(out Texture icon1, out Texture icon2)
	{
		icon1 = null;
		icon2 = null;
	}
}
