//
//  ViewController.swift
//  Lab5_2
//
//  Created by Matthew Seto on 3/11/18.
//  Copyright © 2018 Matthew Seto. All rights reserved.
//
// Thanks to the Mapbox Tutorial: https://www.mapbox.com/install/ios/download-add/ For getting started. 

import UIKit
import Mapbox

class ViewController: UIViewController, MGLMapViewDelegate {
    var mapView: MGLMapView!
    var timer: Timer?
    var polylineSource: MGLShapeSource?
    var currentIndex = 1
    var allCoordinates: [CLLocationCoordinate2D]!
    
    //once the page loads, do this stuff:
    override func viewDidLoad() {
        super.viewDidLoad()
        
        //Make the frame
        mapView = MGLMapView(frame: view.bounds)
        mapView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        //set center/zoom
        mapView.setCenter(
            CLLocationCoordinate2D(latitude: 47.245595, longitude: -122.438780),
            zoomLevel: 13,
            animated: false)
        view.addSubview(mapView)
        
        mapView.delegate = self
        //get the coordinates from the coodinates function (GeoJSON)
        allCoordinates = coordinates()
    }
    
    // Wait until the map is loaded before adding to the map.
    func mapView(_ mapView: MGLMapView, didFinishLoading style: MGLStyle) {
        addLayer(to: style)
        animatePolyline()
    }
    
    func addLayer(to style: MGLStyle) {
        // Add an empty MGLShapeSource, we’ll keep a reference to this and add points to this later.
        let source = MGLShapeSource(identifier: "polyline", shape: nil, options: nil)
        style.addSource(source)
        polylineSource = source
        
        // Add a layer to style our polyline.
        let layer = MGLLineStyleLayer(identifier: "polyline", source: source)
        layer.lineJoin = MGLStyleValue(rawValue: NSValue(mglLineJoin: .round))
        layer.lineCap = MGLStyleValue(rawValue: NSValue(mglLineCap: .round))
        layer.lineColor = MGLStyleValue(rawValue: UIColor.red)
        layer.lineWidth = MGLStyleFunction(interpolationMode: .exponential,
                                           cameraStops: [14: MGLConstantStyleValue<NSNumber>(rawValue: 5),
                                                         18: MGLConstantStyleValue<NSNumber>(rawValue: 20)],
                                           options: [.defaultValue : MGLConstantStyleValue<NSNumber>(rawValue: 1.5)])
        style.addLayer(layer)
    }
    
    func animatePolyline() {
        currentIndex = 1
        
        // Start a timer that will simulate adding points to our polyline. This could also represent coordinates being added to our polyline from another source, such as a CLLocationManagerDelegate.
        timer = Timer.scheduledTimer(timeInterval: 0.05, target: self, selector: #selector(tick), userInfo: nil, repeats: true)
    }
    
    @objc func tick() {
        if currentIndex > allCoordinates.count {
            timer?.invalidate()
            timer = nil
            return
        }
        
        // Create a subarray of locations up to the current index.
        let coordinates = Array(allCoordinates[0..<currentIndex])
        
        // Update our MGLShapeSource with the current locations.
        updatePolylineWithCoordinates(coordinates: coordinates)
        
        currentIndex += 1
    }
    
    func updatePolylineWithCoordinates(coordinates: [CLLocationCoordinate2D]) {
        var mutableCoordinates = coordinates
        
        let polyline = MGLPolylineFeature(coordinates: &mutableCoordinates, count: UInt(mutableCoordinates.count))
        
        // Updating the MGLShapeSource’s shape will have the map redraw our polyline with the current coordinates.
        polylineSource?.shape = polyline
    }
    
    //The coodinates that the line will follow
    func coordinates() -> [CLLocationCoordinate2D] {
        return [
            (-122.438699, 47.247049),
            (-122.437192, 47.247234),
            (-122.436212, 47.243080),
            (-122.432036, 47.233353),
            (-122.415988, 47.238731),
            (-122.410610, 47.239370),
            (-122.412896, 47.244937),
            (-122.439243, 47.242747),
            (-122.438699, 47.247049)
            ].map({CLLocationCoordinate2D(latitude: $0.1, longitude: $0.0)})
    }
}


